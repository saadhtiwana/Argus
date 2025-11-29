import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin
import json

class VulnerabilityScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.vulnerabilities = []

    async def scan_sqli(self, page, url):
        """Scan for SQL Injection vulnerabilities in inputs."""
        print(f"[*] Scanning for SQLi on {url}...")
        
        # Simple payloads
        payloads = ["' OR '1'='1", "' OR '1'='1' --", "admin' --"]
        
        inputs = await page.locator('input').all()
        for i, input_tag in enumerate(inputs):
            # Check if visible and editable
            if not await input_tag.is_visible() or not await input_tag.is_editable():
                continue
                
            input_type = await input_tag.get_attribute('type')
            input_name = await input_tag.get_attribute('name') or ""
            
            # Heuristic: target password fields or text fields
            if input_type == 'password' or 'password' in input_name.lower() or input_type in ['text', 'search']:
                for payload in payloads:
                    try:
                        await input_tag.fill(payload)
                        # Try to find a submit button or press enter
                        # This is tricky in SPAs, often just pressing Enter works
                        await input_tag.press('Enter')
                        
                        # Wait for potential navigation or error message
                        await page.wait_for_timeout(2000) 
                        
                        content = await page.content()
                        if "Welcome" in content or "syntax error" in content.lower() or "database error" in content.lower() or "Invalid email or password" not in content: # Juice shop specific negative check maybe?
                             # For Juice Shop, a successful login usually redirects or shows a basket
                            if "basket" in page.url or "search" not in page.url: # Very rough heuristic
                                pass
                            
                            # Better check for Juice Shop specifically:
                            # If we logged in as admin, we might see "Account" or similar.
                            pass

                        # For generic scanner, let's just log what we tried
                        # Real detection needs more robust oracle
                    except Exception as e:
                        print(f"[!] Error testing SQLi payload: {e}")

    async def scan_xss(self, page, url):
        """Scan for XSS vulnerabilities."""
        print(f"[*] Scanning for XSS on {url}...")
        payload = "<script>alert('XSS')</script>"
        
        inputs = await page.locator('input').all()
        for input_tag in inputs:
             if not await input_tag.is_visible() or not await input_tag.is_editable():
                continue
             
             try:
                await input_tag.fill(payload)
                await input_tag.press('Enter')
                await page.wait_for_timeout(2000)
                
                content = await page.content()
                if payload in content:
                    print(f"[+] Potential XSS found with payload: {payload}")
                    self.vulnerabilities.append({
                        "type": "Cross-Site Scripting (XSS)",
                        "url": url,
                        "payload": payload,
                        "details": "Payload reflected in DOM."
                    })
             except Exception as e:
                 print(f"[!] Error testing XSS: {e}")

    async def run(self):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context(ignore_https_errors=True)
                page = await context.new_page()
                
                print(f"[*] Visiting {self.target_url}")
                try:
                    await page.goto(self.target_url, timeout=60000)
                    await page.wait_for_load_state('domcontentloaded')
                    await page.wait_for_timeout(5000) # Extra wait for SPA
                    
                    # Juice Shop specific: dismiss welcome banner if present
                    try:
                        await page.click('button[aria-label="Close Welcome Banner"]', timeout=2000)
                    except:
                        pass
                    
                    await page.screenshot(path="debug_screenshot.png")
                    print("[*] Saved debug_screenshot.png")
                    
                    title = await page.title()
                    print(f"[*] Page Title: {title}")
                    print(f"[*] Final URL: {page.url}")
                    
                    try:
                        await page.wait_for_selector('input', timeout=10000)
                    except:
                        print("[!] Timed out waiting for inputs.")
                    
                    # Find inputs
                    inputs = await page.locator('input').all()
                    print(f"[*] Found {len(inputs)} inputs on {self.target_url}")
                    
                    content = await page.content()
                    with open("debug_content.html", "w", encoding="utf-8") as f:
                        f.write(content)
                    print("[*] Saved debug_content.html")
                    
                    if len(inputs) > 0:
                        await self.scan_xss(page, self.target_url)
                        # Re-navigate to clear state
                        await page.goto(self.target_url)
                        await page.wait_for_load_state('networkidle')
                        await self.scan_sqli(page, self.target_url)
                        
                except Exception as e:
                    print(f"[!] Error during scan: {e}")
                    with open("error_log.txt", "w") as f:
                        f.write(str(e))
                
                await browser.close()
                self.generate_report()
        except Exception as e:
            print(f"[!] Critical Error: {e}")
            with open("error_log.txt", "w") as f:
                f.write(str(e))

    def generate_report(self):
        print("\n[*] Generating Report...")
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin
import json

class VulnerabilityScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.vulnerabilities = []

    async def scan_sqli(self, page, url):
        """Scan for SQL Injection vulnerabilities in inputs."""
        print(f"[*] Scanning for SQLi on {url}...")
        
        # Simple payloads
        payloads = ["' OR '1'='1", "' OR '1'='1' --", "admin' --"]
        
        inputs = await page.locator('input').all()
        for i, input_tag in enumerate(inputs):
            # Check if visible and editable
            if not await input_tag.is_visible() or not await input_tag.is_editable():
                continue
                
            input_type = await input_tag.get_attribute('type')
            input_name = await input_tag.get_attribute('name') or ""
            
            # Heuristic: target password fields or text fields
            if input_type == 'password' or 'password' in input_name.lower() or input_type in ['text', 'search']:
                for payload in payloads:
                    try:
                        await input_tag.fill(payload)
                        # Try to find a submit button or press enter
                        # This is tricky in SPAs, often just pressing Enter works
                        await input_tag.press('Enter')
                        
                        # Wait for potential navigation or error message
                        await page.wait_for_timeout(2000) 
                        
                        content = await page.content()
                        if "Welcome" in content or "syntax error" in content.lower() or "database error" in content.lower() or "Invalid email or password" not in content: # Juice shop specific negative check maybe?
                             # For Juice Shop, a successful login usually redirects or shows a basket
                            if "basket" in page.url or "search" not in page.url: # Very rough heuristic
                                pass
                            
                            # Better check for Juice Shop specifically:
                            # If we logged in as admin, we might see "Account" or similar.
                            pass

                        # For generic scanner, let's just log what we tried
                        # Real detection needs more robust oracle
                    except Exception as e:
                        print(f"[!] Error testing SQLi payload: {e}")

    async def scan_xss(self, page, url):
        """Scan for XSS vulnerabilities."""
        print(f"[*] Scanning for XSS on {url}...")
        payload = "<script>alert('XSS')</script>"
        
        inputs = await page.locator('input').all()
        for input_tag in inputs:
             if not await input_tag.is_visible() or not await input_tag.is_editable():
                continue
             
             try:
                await input_tag.fill(payload)
                await input_tag.press('Enter')
                await page.wait_for_timeout(2000)
                
                content = await page.content()
                if payload in content:
                    print(f"[+] Potential XSS found with payload: {payload}")
                    self.vulnerabilities.append({
                        "type": "Cross-Site Scripting (XSS)",
                        "url": url,
                        "payload": payload,
                        "details": "Payload reflected in DOM."
                    })
             except Exception as e:
                 print(f"[!] Error testing XSS: {e}")

    async def run(self):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context(ignore_https_errors=True)
                page = await context.new_page()
                
                print(f"[*] Visiting {self.target_url}")
                try:
                    await page.goto(self.target_url, timeout=60000)
                    await page.wait_for_load_state('domcontentloaded')
                    await page.wait_for_timeout(5000) # Extra wait for SPA
                    
                    # Juice Shop specific: dismiss welcome banner if present
                    try:
                        await page.click('button[aria-label="Close Welcome Banner"]', timeout=2000)
                    except:
                        pass
                    
                    await page.screenshot(path="debug_screenshot.png")
                    print("[*] Saved debug_screenshot.png")
                    
                    title = await page.title()
                    print(f"[*] Page Title: {title}")
                    
                    try:
                        await page.wait_for_selector('input', timeout=10000)
                    except:
                        print("[!] Timed out waiting for inputs.")
                    
                    # Find inputs
                    inputs = await page.locator('input').all()
                    print(f"[*] Found {len(inputs)} inputs on {self.target_url}")
                    
                    content = await page.content()
                    with open("debug_content.html", "w", encoding="utf-8") as f:
                        f.write(content)
                    print("[*] Saved debug_content.html")
                    
                    if len(inputs) > 0:
                        await self.scan_xss(page, self.target_url)
                        # Re-navigate to clear state
                        await page.goto(self.target_url)
                        await page.wait_for_load_state('networkidle')
                        await self.scan_sqli(page, self.target_url)
                        
                except Exception as e:
                    print(f"[!] Error during scan: {e}")
                    with open("error_log.txt", "w") as f:
                        f.write(str(e))
                
                await browser.close()
                self.generate_report()
        except Exception as e:
            print(f"[!] Critical Error: {e}")
            with open("error_log.txt", "w") as f:
                f.write(str(e))

    def generate_report(self):
        print("\n[*] Generating Report...")
        with open("vulnerability_report.json", "w") as f:
            json.dump(self.vulnerabilities, f, indent=4)
        print(f"[*] Report saved to vulnerability_report.json")
        print(json.dumps(self.vulnerabilities, indent=4))

if __name__ == "__main__":
    # Example usage
    target_url = "https://juice-shop.herokuapp.com/#/login"
    scanner = VulnerabilityScanner(target_url)
    asyncio.run(scanner.run())
