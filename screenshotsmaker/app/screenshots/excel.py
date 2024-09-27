import io
import time
from pathlib import Path

import pyautogui
import pyperclip
import pythoncom
import pywintypes
import win32com
import win32com.client as win32
import win32gui
from PIL import ImageGrab

from app.screenshots.exceptions import ScreenshotMakerException
from app.services import win32com_util

_XL_MAXIMIZED = -4137


class SheetDoesntExist(ScreenshotMakerException):
    """ Raised when no such worksheet exists. """

    def __init__(self, sheet_name: str):
        super().__init__(f"Invalid sheet name: '{sheet_name}'")


class ExcelScreenshotMaker:

    def __init__(self, *, box: tuple[int, int, int, int] | None = None):
        super().__init__()
        self._box = box

    def make_sheet_screenshots(self, workbook_path: Path) -> list[bytes]:
        result: list[bytes] = []
        excel = self._dispatch_excel()
        try:
            workbook = excel.Workbooks.Open(str(workbook_path.absolute()), ReadOnly=True)

            for i in range(1, workbook.Worksheets.Count + 1):
                ss = self._make_sheet_screenshot(workbook.Worksheets(i))
                result.append(ss)
        finally:
            excel.Quit()
        return result

    def make_sheet_screenshot(self, workbook_path: Path, sheet_name: str) -> bytes:
        excel = self._dispatch_excel()
        try:
            workbook = excel.Workbooks.Open(str(workbook_path.absolute()), ReadOnly=True, UpdateLinks=False)

            worksheet = None
            for i in range(1, workbook.Worksheets.Count + 1):
                ws = workbook.Worksheets(i)
                if sheet_name == ws.Name:
                    worksheet = ws
                    break
            if worksheet is None:
                raise SheetDoesntExist(sheet_name)
            return self._make_sheet_screenshot(worksheet)
        finally:
            try:
                excel.Quit()
            except Exception:
                pass

    def _dispatch_excel(self):
        pythoncom.CoInitialize()
        excel = win32com_util.ensure_dispatch('Excel.Application')
        excel.DisplayAlerts = False
        excel.AskToUpdateLinks = False
        excel.Visible = True
        excel.WindowState = _XL_MAXIMIZED
        return excel

    def _guardian_kill(self):
        pass

    def _make_sheet_screenshot(self, worksheet) -> bytes:
        return self._make_sheet_screenshot_clip(worksheet)

    def _make_sheet_screenshot_true(self, worksheet) -> bytes:
        # excel might require some time to be available
        # for SetForegroundWindow call, so make calls repeatedly
        excel = worksheet.Application

        for i in range(0, 50):
            try:
                win32gui.SetForegroundWindow(excel.Hwnd)
                break
            except pywintypes.error:
                time.sleep(0.05)
        win32gui.SetForegroundWindow(excel.Hwnd)

        worksheet.Activate()
        worksheet.Range("A1").Select()
        worksheet.Application.ActiveWindow.ScrollRow = 1
        worksheet.Application.ActiveWindow.ScrollColumn = 1
        time.sleep(0.2)
        img = pyautogui.screenshot()
        if self._box:
            img = img.crop(box=self._box)
        bio = io.BytesIO()
        img.save(bio, format='PNG')
        bio.seek(0)
        return bio.read()

    def _make_sheet_screenshot_clip(self, worksheet) -> bytes:
        worksheet.Activate()
        # clear clipboard
        pyperclip.copy('')
        worksheet.Range("A1:Z200").CopyPicture(Format=win32com.client.constants.xlBitmap)
        for i in range(0, 20):
            time.sleep(0.1)
            image = ImageGrab.grabclipboard()
            if image:
                break
        else:
            raise ScreenshotMakerException("Failed to copy the sheet to the clipboard")

        if self._box:
            image = image.crop(box=self._box)
        bio = io.BytesIO()
        image.save(bio, format='PNG')
        bio.seek(0)
        return bio.read()
