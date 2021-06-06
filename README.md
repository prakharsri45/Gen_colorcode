# gen_colorcode

To reduce the redundancy in selection of color for website making, project, blogging, newsletter, online graphics etc.  Here the program takes Input as a color name and give the output in color code. Also, we can see colors with the respective code in the plot generated after the execution of the program.  The program works accurately and generates RGB code, HSL code and Hex code.  

**For example:**  

Do wanna enter color names or see all colors. (?custom/all): custom  
Enter the color name: dark strong purplish red  
Do wanna enter more enter more color names. (?y/n): y  
Enter the color name: light bit yellow  
Do wanna enter more enter more color names. (?y/n): n  

dark strong purplish_red, rgb=> [167, 24, 44] , hsl=> [351.4286, 75, 37.5] , hex=> #a7182c  
light bit yellow, rgb=> [183, 183, 135] , hsl=> [60.0, 25, 62.5] , hex=> #b7b787  
Total number of different color codes generated: 2  
Total number of all color codes generated: 2  
Execution time: 92.1879 seconds  

***Note:*** Execution time is high due to the graph  

![Figure_1](https://user-images.githubusercontent.com/81968507/116821831-77743980-ab49-11eb-93ba-5750339c5993.png)


# How to find files:
1.) Lark folder have lark module (library).  
2.) Color_code.py file contain python code of the project.  
3.) Color_code.da file contain DistAlgo code of the project.  
4.) Format.jpg holds the picture that demonstrates a tree of color.  
5.) The third file Output file, it has output of the entire multiple color names with code. However, program prints and display graph in the output after running it in jupyter/python/pycharm.  
6.) Report.pdf, this file contains all the informations.  
7.) Readme.md file have running and some other stuff.  


# Main libraries required for the project:
1.) Lark module, for parsing name using context-free grammar. Lark is used instead of tpg because Lark is user friendly, efficient and handle ambiguity gracefully. [For more details, visit: https://github.com/lark-parser/lark].  
2.) Enum, for specifying the color value.  
3.) Time, used to calculate the execution time.  
4.) Itertools, used to make multiple names for testing. [For creating input names].  
5.) Matplotlib, used to create scattered colors in the graph.  
6.) Mplcursors, used to display hovering in the graph with color name and code.  


# How to run the program:
1.) Use jupyter/pycharm/python to run the program.  
2.) Install all module mentioned above especially Lark module.  
3.) Currently, program is creating multiple names automatically but we can customize it. These names are used as input color names.  
4.) Run the program in the IDE.  
5.) Then it will ask, all or custom: a.) If entered all, each and every possible colors presents in the grammar will print. b.) If entered custom, then it will ask to enter color names. c.) After that if ask for more entry of color name.  
6.) When the search result complete, color code generated after parsing and analyzing the color names. Color names are present in the output along with RGB code, HSL code and Hex code. Also, after few second colors will display in the graph with their names and code (When mouse hover on then).  
7.) It will also display the total number of color code generated and execution time.  


# Most Interesting thing:
1.) This program also runs in DistAlgo.  
2.) The file color_code.da has the program and in the terminal writes "python -m da color_code.da" then presses enter.  
3.) Program will generate the color code and graph same as in python.  


# How to Enter color name:
1.) First enter the lightness word (optional).  
2.) After that enter the saturation condition word, which is mentioned above (optional).  
3.) At last, write basic color name from three lists of color pattern:  
   -   General color name.  
   -   Half hue color name.  
   -   Quarter hue color name.  

4.) Press ENTER.  


