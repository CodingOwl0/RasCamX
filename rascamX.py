from rascam import Ras_Cam,Joystick_Motion_type,Joystick_Motion_Val,RGB_Matrix,set_screen_brightness,run_command,power_val
import time
## By LUCA FRANZISKOWSKI - RascamX
## This Program combines many example scripts from Sunfounder.
## VERSION 0.1, 11.09.2022

## HOW-TO USE
#   Press Cursor: Change Brightness of screen
#   Cursor Up   : Change Picture-Mode
#   Cursor Down : Change Picture-Mode
#   Cursor Left : Change Image-Filter
#   Cursor Right: Change Image-Filter

#   Press Cursor > 10sec : Open / Close settings
#   Cursor Up   : Change Setting-Value
#   Cursor Down : Change Setting-Value
#   Cursor Left : Move to other setting
#   Cursor Right: Move to other setting


## camera_setting,you can diy by yourself.just add new item to the dict.Like the one shown below.
camera_setting_dict = {
        "resolution":[(640,480),(1280,960),(1920,1440),(2592,1944)],    
        "rotation":[0,90,180,270],      #
        "brightness":[i for i in range(0,101)],   # 0~100  default 50
        "sharpness":[i for i in range(-100,101)],    # -100~100  default 0
        "contrast":[i for i in range(-100,101)],    # -100~100  default 0
        "saturation":[i for i in range(-100,101)],    # -100~100  default 0
        "iso":[0,100,200,320,400,500,640,800],           #Vaild value:0(auto) 100,200,320,400,500,640,800
        "exposure_compensation":[i for i in range(-10,11)],       # -25~25  default 0
        "exposure_mode":['off', 'auto','night', 'nightpreview','backlight', 'spotlight', 'sports', 'snow', 'beach','verylong', 'fixedfps', 'antishake','fireworks'],       #Valid values are: 'off', 'auto' (default),'night', 'nightpreview', 'backlight', 'spotlight', 'sports', 'snow', 'beach','verylong', 'fixedfps', 'antishake', or 'fireworks'
        "meter_mode":['average','spot', 'backlit', 'matrix'],     #Valid values are: 'average' (default),'spot', 'backlit', 'matrix'.
        "awb_mode":['off', 'auto', 'sunlight', 'cloudy', 'shade', 'tungsten', 'fluorescent','incandescent', 'flash', 'horizon'],       #'off', 'auto' (default), ‘sunlight', 'cloudy', 'shade', 'tungsten', 'fluorescent','incandescent', 'flash', or 'horizon'.
        "drc_strength":['off', 'low', 'medium', 'high'],
}



if __name__ == "__main__":
    try:
        Ras_Cam.camera_start()
        Ras_Cam.human_detect_switch(True)
        
        ## Variables
        rr = RGB_Matrix(0X74)
        setting_menu_flag = False           # if the user pressed long enough before, he can edit settings
        setting_menu_time = 10              # time, which the user needs to press to open and close the settings
        setting_font_coordinates = (10,22)
        position_mode_txt = (0,230)         # Position of the mode-description
        position_brightness_txt = (250,230) # Position of the brightness-text
        
        horizontal_flag = True
        camera_type = 'resolution'
        camera_val = (1920,1440)  # set the the init resolution 
        
        picture_type = 1
        picture_options = 3
        display_brightness = 25
        total_time = 8
        content_1_color = [98,150,124]   ## content 1 text color ([R,G,B])
        font_size = 0.5    ## content font size   (The best range is 0.5 ~ 0.8)
        face_detection = False
        
        while True:
            
            press_counter = 0
            button_type = Joystick_Motion_type()
            
            if button_type == 'shuttle': #Ausloeser gedrueckt
                if picture_type == 1:  #Take photo with flash
                    rr.draw_line([1,8],fill=(255,255,255))
                    rr.display() # open the rgb
                    time.sleep(0.5)
                    Ras_Cam.shuttle_button(True)
                    time.sleep(0.5)
                    rr.draw_line([1,8],fill=(0,0,0)) # close the rgb
                    rr.display()
                    
                elif picture_type == 2: #Take photo with timer 8 seconds
                    for i in range(9):
                        if i == 8:
                            rr.draw_line((1,8),fill=(0,255,0))
                            rr.display()
                            break
                        rr.draw_point((i),fill=(255,0,0))
                        rr.display()
                        time.sleep(float(total_time) / 8)  
                    Ras_Cam.shuttle_button(True)
                    time.sleep(1)
                    rr.draw_line((1,8),fill=(0,0,0))
                    rr.display()
                    
                elif picture_type == 3 or picture_type == 4:
                    Ras_Cam.shuttle_button(True)
                    time.sleep(1)
                    
            elif button_type == 'up': #      ------> PHOTO-MODE UP
                if setting_menu_flag == False:
                    if picture_type < picture_options:
                        picture_type +=  1
                    elif picture_type > picture_options or picture_type == picture_options: #      ------> PHOTO-MODE DOWN
                        picture_type = 1
                    print('Changing mode to ' + str(picture_type))
                    
                elif setting_menu_flag == True:
                    camera_type,camera_val = Ras_Cam.change_show_setting(shirt_way = 'None')
                    print(camera_type,camera_val)
                    setting_choice_num = len(camera_setting_dict[camera_type])
                    setting_val_index = camera_setting_dict[camera_type].index(camera_val)
                    if setting_val_index < setting_choice_num-1:
                        setting_val_index += 1
                    Ras_Cam.change_setting_type_val(camera_type,camera_setting_dict[camera_type][setting_val_index])          #change the current setting
                    
            elif button_type == 'down':
                if setting_menu_flag == False:
                    if picture_type > 1:
                        picture_type -= 1
                    elif picture_type == 1:
                        picture_type = picture_options
                    print('Changing mode to ' + str(picture_type))
                    
                elif setting_menu_flag == True:
                    camera_type,camera_val = Ras_Cam.change_show_setting(shirt_way = 'None')
                    print(camera_type,camera_val)
                    setting_val_index = camera_setting_dict[camera_type].index(camera_val)
                    if setting_val_index > 0:
                        setting_val_index -= 1
                    Ras_Cam.change_setting_type_val(camera_type,camera_setting_dict[camera_type][setting_val_index])          #change the current setting
            
            elif button_type == 'left':
                if setting_menu_flag == False:
                    Ras_Cam.photo_effect('sub') # -----> PHOTO-EFECT CHANGE - Left shift switch.
                elif setting_menu_flag == True:
                    camera_type,camera_val = Ras_Cam.change_show_setting(shirt_way = 'add')   #Toggle the round button to the left or right.it will return the camera current setting type
            
            elif button_type == 'right':
                if setting_menu_flag == False:
                    Ras_Cam.photo_effect('add') # -----> PHOTO-EFECT CHANGE - Right shift switch.
                elif setting_menu_flag == True:
                    camera_type,camera_val = Ras_Cam.change_show_setting(shirt_way = 'sub')

            elif button_type == 'press':    # -----> CHANGE DISPLAY-BRIGHTNESS (4 Steps)
                while Joystick_Motion_Val('press') == 0: ##----> Misst, wie lange der Button gedrueckt wird
                    print("Pressed: ",press_counter)
                    press_counter += 1
                    count = 0
                    if press_counter >= setting_menu_time:
                        break
                    time.sleep(0.1)
                    
                if press_counter >= setting_menu_time:
                    setting_menu_flag = not setting_menu_flag
                    Ras_Cam.show_setting(setting_menu_flag)   #show camera setting
                    
                elif press_counter < setting_menu_time: ##----> Wurde vor den 2 sek abgebrochen
                    if display_brightness == 25:
                        display_brightness = 50
                    elif display_brightness == 50:
                        display_brightness = 75
                    elif display_brightness == 75:
                        display_brightness = 100
                    elif display_brightness == 100:
                        display_brightness = 25
                    set_screen_brightness(display_brightness) # set screen brightness (0~100).
                    print('Screen-brightness set to ' + str(display_brightness))
                    Ras_Cam.show_content(2, str(display_brightness), position_brightness_txt,content_1_color, font_size)
                
            # Anzeige schliesslich aktualisieren:
            if  picture_type == 1:
                Ras_Cam.show_content(1, "<Flash>", position_mode_txt,content_1_color, font_size)
            elif picture_type == 2:
                Ras_Cam.show_content(1, "<Timer>", position_mode_txt,content_1_color, font_size)
            elif picture_type == 3:
                Ras_Cam.show_content(1, "<Auto>", position_mode_txt,content_1_color, font_size)
            elif picture_type == 4:
                Ras_Cam.show_content(1, "<Face>", position_mode_txt,content_1_color, font_size)
            
            if face_detection == True:
                human_face_num = Ras_Cam.human_detect_object_num()
                if human_face_num > 0:
                    print("I find %d people !!!" % human_face_num)
                    rr.draw_line((1,8),fill=(0,255,0))
                    rr.display()
                else:
                    rr.draw_line((1,8),fill=(255,0,0))
                    rr.display()
    
    except:
        print("An error occured. Exiting...")
        
    finally:
        run_command("sudo kill $(ps aux | grep 'rascamX.py' | awk '{ print $2 }')")