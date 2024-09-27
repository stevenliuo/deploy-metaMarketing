import io
import logging
import os.path
import re
import shutil
import tempfile
import time
from pathlib import Path

import pyautogui
import pythoncom

from app.screenshots.exceptions import ScreenshotMakerException
from app.services import win32com_util

logger = logging.getLogger(__name__)


PP_WINDOW_MAXIMIZED = 3


class SlideDoesntExist(ScreenshotMakerException):
    """ Raised when no such slide exists. """

    def __init__(self, slide_name: str):
        super().__init__(f"Invalid slide name: '{slide_name}'")


class PowerPointBringToFrontException(ScreenshotMakerException):
    """ Raised when not possible to bring PP to the front """

    def __init__(self):
        super().__init__("Can't bring PowerPoint to the front")


class PowerPointScreenshotMaker:

    def __init__(self, *, box: tuple[int, int, int, int] | None = None):
        super().__init__()
        self._box = box

    def make_slides_screenshots(self, presentation_path: Path) -> list[bytes]:
        pythoncom.CoInitialize()
        # powerpoint = win32.gencache.EnsureDispatch('Powerpoint.Application')
        powerpoint = win32com_util.ensure_dispatch('Powerpoint.Application')
        try:
            powerpoint.Visible = True
            powerpoint.WindowState = PP_WINDOW_MAXIMIZED
            powerpoint.Activate()

            presentation = powerpoint.Presentations.Open(str(presentation_path.absolute()), ReadOnly=True)
            return self._make_slides_images(presentation)
        finally:
            powerpoint.Quit()
            del powerpoint

    def _make_slides_screenshots(self, presentation) -> list[bytes]:
        shots = []
        slide_count = presentation.Slides.Count
        # Preload all slides
        for slide_index in range(1, slide_count + 1):
            presentation.Slides(slide_index).Select()

        for slide_index in range(1, slide_count + 1):
            presentation.Slides(slide_index).Select()
            time.sleep(0.2)
            shots.append(self._make_slide_screenshot())

        return shots

    def _make_slides_images(self, presentation) -> list[bytes]:
        def extract_int(s: str, default: int | None = None):
            match = re.search(r'\d+', s)
            if match:
                return int(match.group())
            else:
                return default

        result = []
        target_dir = None
        try:
            target_dir = tempfile.mktemp(prefix="pp_ss_", suffix=str(int(time.time())))
            presentation.Export(target_dir, "png")
            files = [f for f in Path(target_dir).glob("*.png")]
            files.sort(key=lambda f: extract_int(f.name))

            for f in files:
                result.append(f.read_bytes())
        finally:
            if target_dir and os.path.isdir(target_dir):
                try:
                    shutil.rmtree(target_dir)
                except Exception as e:
                    logger.warning(f"Failed to cleanup slides dir: {e}")

        return result

    def _make_slide_screenshot(self) -> bytes:
        img = pyautogui.screenshot()
        if self._box:
            img = img.crop(box=self._box)
        bio = io.BytesIO()
        img.save(bio, format='PNG')
        bio.seek(0)
        return bio.read()


class SlidesCopier:

    def duplicate_slides(self, presentation_path: Path, save_path: Path, total_count: int):
        pythoncom.CoInitialize()
        powerpoint = win32com_util.ensure_dispatch('Powerpoint.Application')
        try:
            powerpoint.Visible = True
            powerpoint.WindowState = PP_WINDOW_MAXIMIZED
            powerpoint.Activate()

            presentation = powerpoint.Presentations.Open(str(presentation_path.absolute()))
            self._duplicate_slides(presentation, total_count, save_path)
        finally:
            powerpoint.Quit()
            del powerpoint

    def _duplicate_slides(self, presentation, total_count: int, save_path: Path):
        while presentation.Slides.Count < total_count:
            presentation.Slides(presentation.Slides.Count).Duplicate()
        presentation.SaveAs(str(save_path.absolute()))

if __name__ == "__main__":
    sc = SlidesCopier()
    s = Path("c:\\data\\2.pptx")
    t = Path("c:\\data\\dup.pptx")
    sc.duplicate_slides(s, t, 10)