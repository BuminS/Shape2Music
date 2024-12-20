% Clean up the workspace
clear all;  % Remove all variables
clc;        % Clear the command window
close all;  % Close all open figures
%% Shape to music, Buminhan Sansa

% Step 1: Open a file selection dialog to choose the image
% [filename, pathname] = uigetfile({'*.png'}, 'Select a PNG Image');

% Step 2: Load the image
%imread gives 3 variables, img, alpha and map. reads the indexed image in filename into A and 
% reads the associated colormap of the image into map. Colormap values in the image file are 
% automatically rescaled into the range [0, 1]. alpha additionally returns the image transparency. 
% This syntax applies only to PNG, For PNG files, transparency is the alpha channel, if one is present.
%% Shape to music, Buminhan Sansa
%image load from file, use RGB input only!
img_raw = imread("image_13_input_RGB.png");
figure
imshow(img_raw)
title('Original Image - Selected by User');
%img cropping to show only spinodoid
img = img_raw(65:530,317:783,:);
figure
imshow(img)
title('Cropped Image - Selected by User');
%Img resizing for shorter song duration
Img = imresize(img, [150, 150]);
figure
imshow(Img)
title('Resized Image for music - Selected by User');


% Step 4: Define frequency ranges for each color channel
R_min = 50;   R_max = 300;   % Red mapped to 50-300 Hz (Represents Bass and Sub Bass)
G_min = 301;  G_max = 1000;   % Green mapped to 301-1000 Hz (Lower Midrange)
B_min = 1001;  B_max = 4500;  % Blue mapped to 8000-10,000 Hz (Higher midrange and Presence)

% Sound parameters
fs = 10100;  % Sampling frequency
base_duration = 0.15;  % Base duration for each note in seconds

% Initialize the music array
music = [];

% Step size for pixel processing (to avoid dense sound)
%Used in Step 5 for music generation, gets values every 7 pixel 
step = 7;

% Step 5: Generate music from the image
for i = 1:step:size(Img, 1)
    for j = 1:step:size(Img, 2)
        % Nested for-loop for iterating each row for stepsize 
        pixel = double(Img(i, j, :)) / 255;
        % This pixel variable captures the x and y value of the pixel with
        % i and j, then : allows for the pixel variable to capture all 3
        % RGB values. Double()/255 allows easier computation which are originally in
        % the range of 255 then changed to 0-1 (kind of like desnity)
        R_freq = R_min + (R_max - R_min) * pixel(1);
        G_freq = G_min + (G_max - G_min) * pixel(2);
        B_freq = B_min + (B_max - B_min) * pixel(3);
        % converts back to hertz in the thousands range not 0-1.

        freq = mean([R_freq, G_freq, B_freq]);  % Average frequency for all 3
        % different colors in pixels.


        % Generate sine wave for the frequency
        t = 0:1/fs:base_duration;
        note = sin(2 * pi * freq * t);

         % Optional: Display the frequency for debugging for each step
         % pxiel
        fprintf('Pixel (%d, %d): R_freq = %.2f, G_freq = %.2f, B_freq = %.2f, Combined = %.2f Hz\n', ...
                i, j, R_freq, G_freq, B_freq, freq);

        % Add the note and a short pause to the music
        music = [music, note, zeros(1, fs * 0.02)];
    end
end
%fplot(@(x) freq(x));
disp('Code is finished')
sound(music, fs);
%audiowrite('spinodoid_song_image_25.wav', music, fs);
disp('Song saved as spinodoid_song_1.wav');
