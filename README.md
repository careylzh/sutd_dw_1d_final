# OrderNow - sutd_dw_1d_final
IOT-based Food ordering system for our school canteen as part of a non-commercial school design and coding project. 

This is purely a project for educational purposes only. Credits to all parties for providing images and knowledge for making this school graded project possible. 

Implemented on Python 3.7 </br> 
Architecture of Firebase interface with Kivy: S.Chua </br> 
Firebase implementation: S. Chua. Ng. Z.H, Carey Lai </br> 
Python Kivy UI Wireframing: S. Chua </br> 
Python Kivy UI Design: S. Chua, Ng. Z.H, Carey Lai </br> 
Hardware(eletromagnetic lock interface with Arduino and RPi): Zeng. Z.M, Xie. P.N </br> 
Building into Android app: Carey Lai

For anyone interested, you can launch this prototype on your phone via Kivy Launcher by placing these files in the same folder. You will also need to deploy the merchant's screen on another device, + set up a firebase. The images of the various food items are not uploaded for copyright reasons. 

# Future Improvement</br> 
Centrally controlled electromagnetic lock over on-site physical unlocking: In order to streamline the user experience of food collection, we could allow the user to unlock the locker through their phones, instead of implementing a physical screen for unlocking. This will also ensure good hygiene as the users can perform "hands-free" unlocking, minimising contact with the locker. However, our server must now take into consideration that only users with placed orders are allowed to unlock the locker. Implementation could be done in the form of hashing locally on the phones, then using the hash value to verify with that of the current order prepared. 

![SUTD Digital World 2019 Poster](https://github.com/careylzh/sutd_dw_1d_final/blob/master/f03_ordernow_poster.png)
