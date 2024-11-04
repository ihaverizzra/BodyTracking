import psutil
import pyautogui
import time
import keyboard

def list_open_applications():
    applications = []
    for proc in psutil.process_iter(['pid', 'name']):
        applications.append(proc.info)
    return applications

def display_applications(applications):
    print("Open Applications:")
    for index, app in enumerate(applications):
        print(f"{index + 1}: {app['name']} (PID: {app['pid']})")

def search_applications(applications, query):
    matches = []
    for app in applications:
        if query.lower() in app['name'].lower():
            matches.append(app)
    return matches

def monitor_application(app_info):
    try:
        print(f"Starting monitoring for: {app_info['name']} (PID: {app_info['pid']})")
        windows = pyautogui.getWindowsWithTitle(app_info['name'])
        
        if not windows:
            print(f"No window found for {app_info['name']}")
            return
            
        app_window = windows[0]
        app_window.activate()
        print(f"Successfully activated window: {app_window.title}")
        
        while True:
            screenshot = pyautogui.screenshot(region=(app_window.left, app_window.top, 
                                                    app_window.width, app_window.height))
            if screenshot.getpixel((app_window.width // 2, app_window.height // 2)) != (255, 255, 255):
                print("Movement detected! Locking cursor...")
                break
            time.sleep(1)
    except Exception as e:
        print(f"Error in monitor_application: {str(e)}")

if __name__ == "__main__":
    applications = list_open_applications()
    
    while True:
        user_input = input("Type in a number to monitor an application (or press 'q' to search for a certain application): ")
        
        if user_input.lower() == 'q':
            search_query = input("Enter the application name to search: ")
            search_results = search_applications(applications, search_query)
            
            if search_results:
                print("Search Results:")
                for i, app in enumerate(search_results):
                    print(f"{i + 1}: {app['name']} (PID: {app['pid']})")
                
                try:
                    selected = int(input("Type in the number of the application you want to monitor: "))
                    if 1 <= selected <= len(search_results):
                        selected_app = search_results[selected - 1]  # Adjust for 0-based indexing
                        monitor_application(selected_app)
                    else:
                        print(f"Please enter a number between 1 and {len(search_results)}")
                except ValueError:
                    print("Please enter a valid number")
            else:
                print("No applications found with that name.")
        else:
            try:
                selected = int(user_input)
                if 1 <= selected <= len(applications):
                    monitor_application(applications[selected - 1])
                else:
                    print(f"Please enter a number between 1 and {len(applications)}")
            except ValueError:
                print("Please enter a valid number")



