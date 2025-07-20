import os
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from PIL import Image, ImageChops, ImageDraw, ImageFont
import imagehash
import cv2
import numpy as np

from core.config_manager import config
from utils.logger import get_logger


class ScreenshotManager:
    """Advanced screenshot manager with visual testing capabilities"""
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger(__name__)
        self.screenshot_config = config.get_screenshot_config()
        self.visual_config = config.get_visual_testing_config()
        
        # Create screenshot directory
        self.screenshot_path = Path(self.screenshot_config.get('path', 'screenshots'))
        self.screenshot_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.screenshot_path / 'success').mkdir(exist_ok=True)
        (self.screenshot_path / 'failed').mkdir(exist_ok=True)
        (self.screenshot_path / 'baseline').mkdir(exist_ok=True)
        (self.screenshot_path / 'comparison').mkdir(exist_ok=True)
        (self.screenshot_path / 'visual').mkdir(exist_ok=True)
    
    def take_screenshot(self, name: str, full_page: Optional[bool] = None, 
                       quality: Optional[int] = None) -> str:
        """
        Take a screenshot and save it
        
        Args:
            name: Name for the screenshot file
            full_page: Whether to take full page screenshot
            quality: JPEG quality (1-100)
            
        Returns:
            Path to the saved screenshot
        """
        try:
            # Get configuration
            full_page = full_page if full_page is not None else self.screenshot_config.get('full_page', True)
            quality = quality or self.screenshot_config.get('quality', 90)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            
            # Determine save path based on name
            if 'error' in name.lower() or 'failed' in name.lower():
                save_path = self.screenshot_path / 'failed' / filename
            elif 'success' in name.lower():
                save_path = self.screenshot_path / 'success' / filename
            else:
                save_path = self.screenshot_path / filename
            
            # Take screenshot
            if full_page:
                self._take_full_page_screenshot(save_path)
            else:
                self.driver.save_screenshot(str(save_path))
            
            # Optimize image quality
            self._optimize_image(save_path, quality)
            
            self.logger.info(f"Screenshot saved: {save_path}")
            return str(save_path)
            
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise
    
    def _take_full_page_screenshot(self, save_path: Path) -> None:
        """Take full page screenshot"""
        try:
            # Get page dimensions
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            viewport_width = self.driver.execute_script("return window.innerWidth")
            
            # Set window size to viewport size
            self.driver.set_window_size(viewport_width, viewport_height)
            
            # Create full page image
            full_image = Image.new('RGB', (viewport_width, total_height))
            
            # Scroll and capture
            current_position = 0
            while current_position < total_height:
                # Scroll to position
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(0.2)  # Wait for scroll to complete
                
                # Take screenshot of current viewport
                temp_path = save_path.with_suffix('.temp.png')
                self.driver.save_screenshot(str(temp_path))
                
                # Open and crop to viewport
                viewport_image = Image.open(temp_path)
                
                # Calculate crop area
                crop_height = min(viewport_height, total_height - current_position)
                viewport_image = viewport_image.crop((0, 0, viewport_width, crop_height))
                
                # Paste into full image
                full_image.paste(viewport_image, (0, current_position))
                
                current_position += viewport_height
                
                # Clean up temp file
                temp_path.unlink(missing_ok=True)
            
            # Save full page image
            full_image.save(save_path, 'PNG', optimize=True)
            
        except Exception as e:
            self.logger.error(f"Failed to take full page screenshot: {str(e)}")
            # Fallback to regular screenshot
            self.driver.save_screenshot(str(save_path))
    
    def _optimize_image(self, image_path: Path, quality: int) -> None:
        """Optimize image quality and size"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Save with optimization
                img.save(image_path, 'PNG', optimize=True, quality=quality)
        except Exception as e:
            self.logger.warning(f"Failed to optimize image: {str(e)}")
    
    def take_element_screenshot(self, element_locator: Tuple[str, str], name: str) -> str:
        """Take screenshot of specific element"""
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # Wait for element
            wait = WebDriverWait(self.driver, config.get_timeout())
            element = wait.until(EC.presence_of_element_located(element_locator))
            
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # Take full screenshot first
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_path = self.screenshot_path / f"temp_{timestamp}.png"
            self.driver.save_screenshot(str(temp_path))
            
            # Crop to element
            element_location = element.location
            element_size = element.size
            
            with Image.open(temp_path) as img:
                # Calculate crop coordinates
                left = element_location['x']
                top = element_location['y']
                right = left + element_size['width']
                bottom = top + element_size['height']
                
                # Crop image
                cropped_img = img.crop((left, top, right, bottom))
                
                # Save cropped image
                filename = f"{name}_{timestamp}.png"
                save_path = self.screenshot_path / filename
                cropped_img.save(save_path, 'PNG', optimize=True)
            
            # Clean up temp file
            temp_path.unlink(missing_ok=True)
            
            self.logger.info(f"Element screenshot saved: {save_path}")
            return str(save_path)
            
        except Exception as e:
            self.logger.error(f"Failed to take element screenshot: {str(e)}")
            raise
    
    def compare_screenshots(self, baseline_path: str, current_path: str, 
                          tolerance: Optional[float] = None) -> Dict[str, Any]:
        """
        Compare two screenshots and return comparison results
        
        Args:
            baseline_path: Path to baseline screenshot
            current_path: Path to current screenshot
            tolerance: Similarity tolerance (0-1)
            
        Returns:
            Dictionary with comparison results
        """
        try:
            tolerance = tolerance or self.visual_config.get('tolerance', 0.95)
            
            # Load images
            baseline_img = Image.open(baseline_path)
            current_img = Image.open(current_path)
            
            # Ensure same size
            if baseline_img.size != current_img.size:
                current_img = current_img.resize(baseline_img.size, Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if baseline_img.mode != 'RGB':
                baseline_img = baseline_img.convert('RGB')
            if current_img.mode != 'RGB':
                current_img = current_img.convert('RGB')
            
            # Calculate hash similarity
            baseline_hash = imagehash.average_hash(baseline_img)
            current_hash = imagehash.average_hash(current_img)
            hash_similarity = 1 - (baseline_hash - current_hash) / 64.0
            
            # Calculate structural similarity
            baseline_array = np.array(baseline_img)
            current_array = np.array(current_img)
            
            # Convert to grayscale for SSIM
            baseline_gray = cv2.cvtColor(baseline_array, cv2.COLOR_RGB2GRAY)
            current_gray = cv2.cvtColor(current_array, cv2.COLOR_RGB2GRAY)
            
            # Calculate SSIM
            ssim_score = self._calculate_ssim(baseline_gray, current_gray)
            
            # Calculate pixel difference
            diff_img = ImageChops.difference(baseline_img, current_img)
            diff_array = np.array(diff_img)
            pixel_diff_percentage = (np.sum(diff_array > 0) / diff_array.size) * 100
            
            # Determine if images are similar
            is_similar = hash_similarity >= tolerance and ssim_score >= tolerance
            
            # Create difference image
            diff_path = self._create_difference_image(baseline_img, current_img, baseline_path)
            
            result = {
                'similar': is_similar,
                'hash_similarity': hash_similarity,
                'ssim_score': ssim_score,
                'pixel_diff_percentage': pixel_diff_percentage,
                'tolerance': tolerance,
                'difference_image': diff_path,
                'baseline_path': baseline_path,
                'current_path': current_path
            }
            
            self.logger.info(f"Screenshot comparison completed. Similar: {is_similar}, "
                           f"Hash similarity: {hash_similarity:.3f}, SSIM: {ssim_score:.3f}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to compare screenshots: {str(e)}")
            raise
    
    def _calculate_ssim(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate Structural Similarity Index"""
        try:
            # Ensure images are the same size
            if img1.shape != img2.shape:
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
            
            # Calculate SSIM
            ssim = cv2.compareSSIM(img1, img2)
            return ssim
        except Exception:
            # Fallback to simple correlation
            return np.corrcoef(img1.flatten(), img2.flatten())[0, 1]
    
    def _create_difference_image(self, baseline_img: Image.Image, current_img: Image.Image, 
                                baseline_path: str) -> str:
        """Create difference image highlighting changes"""
        try:
            # Calculate difference
            diff_img = ImageChops.difference(baseline_img, current_img)
            
            # Convert to grayscale and enhance differences
            diff_gray = diff_img.convert('L')
            diff_array = np.array(diff_gray)
            
            # Create highlighted difference image
            highlighted = np.zeros_like(diff_array)
            highlighted[diff_array > 30] = 255  # Threshold for significant differences
            
            # Convert back to PIL Image
            highlighted_img = Image.fromarray(highlighted)
            
            # Create RGB version with red highlights
            result_img = baseline_img.copy()
            result_array = np.array(result_img)
            result_array[highlighted == 255] = [255, 0, 0]  # Red for differences
            
            # Save difference image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            diff_filename = f"diff_{Path(baseline_path).stem}_{timestamp}.png"
            diff_path = self.screenshot_path / 'comparison' / diff_filename
            diff_path.parent.mkdir(exist_ok=True)
            
            Image.fromarray(result_array).save(diff_path, 'PNG')
            
            return str(diff_path)
            
        except Exception as e:
            self.logger.error(f"Failed to create difference image: {str(e)}")
            return ""
    
    def save_baseline(self, screenshot_path: str, name: str) -> str:
        """Save screenshot as baseline for visual testing"""
        try:
            baseline_path = self.screenshot_path / 'baseline' / f"{name}.png"
            baseline_path.parent.mkdir(exist_ok=True)
            
            # Copy screenshot to baseline
            import shutil
            shutil.copy2(screenshot_path, baseline_path)
            
            self.logger.info(f"Baseline saved: {baseline_path}")
            return str(baseline_path)
            
        except Exception as e:
            self.logger.error(f"Failed to save baseline: {str(e)}")
            raise
    
    def annotate_screenshot(self, screenshot_path: str, annotations: List[Dict[str, Any]]) -> str:
        """Add annotations to screenshot"""
        try:
            with Image.open(screenshot_path) as img:
                draw = ImageDraw.Draw(img)
                
                # Try to load a font
                try:
                    font = ImageFont.truetype("arial.ttf", 16)
                except:
                    font = ImageFont.load_default()
                
                for annotation in annotations:
                    annotation_type = annotation.get('type', 'rectangle')
                    x1, y1, x2, y2 = annotation.get('coordinates', [0, 0, 100, 100])
                    color = annotation.get('color', 'red')
                    text = annotation.get('text', '')
                    
                    if annotation_type == 'rectangle':
                        draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
                        if text:
                            draw.text((x1, y1 - 20), text, fill=color, font=font)
                    
                    elif annotation_type == 'circle':
                        draw.ellipse([x1, y1, x2, y2], outline=color, width=2)
                        if text:
                            draw.text((x1, y1 - 20), text, fill=color, font=font)
                    
                    elif annotation_type == 'arrow':
                        draw.line([x1, y1, x2, y2], fill=color, width=3)
                        if text:
                            draw.text((x2 + 5, y2), text, fill=color, font=font)
                
                # Save annotated image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                annotated_path = screenshot_path.replace('.png', f'_annotated_{timestamp}.png')
                img.save(annotated_path, 'PNG')
                
                self.logger.info(f"Annotated screenshot saved: {annotated_path}")
                return annotated_path
                
        except Exception as e:
            self.logger.error(f"Failed to annotate screenshot: {str(e)}")
            raise
    
    def create_screenshot_report(self, screenshots: List[Dict[str, Any]]) -> str:
        """Create HTML report with screenshots"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.screenshot_path / f"screenshot_report_{timestamp}.html"
            
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Screenshot Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .screenshot { margin: 20px 0; border: 1px solid #ccc; padding: 10px; }
                    .screenshot img { max-width: 100%; height: auto; }
                    .metadata { background: #f5f5f5; padding: 10px; margin: 10px 0; }
                    .success { border-left: 5px solid green; }
                    .failed { border-left: 5px solid red; }
                </style>
            </head>
            <body>
                <h1>Screenshot Report</h1>
                <p>Generated: {timestamp}</p>
            """.format(timestamp=timestamp)
            
            for screenshot in screenshots:
                status_class = 'success' if screenshot.get('status') == 'success' else 'failed'
                html_content += f"""
                <div class="screenshot {status_class}">
                    <h3>{screenshot.get('name', 'Screenshot')}</h3>
                    <div class="metadata">
                        <p><strong>Path:</strong> {screenshot.get('path', '')}</p>
                        <p><strong>Status:</strong> {screenshot.get('status', 'unknown')}</p>
                        <p><strong>Timestamp:</strong> {screenshot.get('timestamp', '')}</p>
                        <p><strong>Reason:</strong> {screenshot.get('reason', '')}</p>
                    </div>
                    <img src="{screenshot.get('path', '')}" alt="{screenshot.get('name', 'Screenshot')}">
                </div>
                """
            
            html_content += """
            </body>
            </html>
            """
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Screenshot report created: {report_path}")
            return str(report_path)
            
        except Exception as e:
            self.logger.error(f"Failed to create screenshot report: {str(e)}")
            raise 