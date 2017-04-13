using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace Events {


    public delegate void ButtonEventHandler(Object sender, ButtonEventArgs args);


    public static class ButtonEvents {

        static public Game1.Game1 game1;

        static public void changeMenu(Object sender, ButtonEventArgs e) {
            if (e.command == "mainmenu") {
                game1.menuHandler.currentMenu = game1.menuHandler.mainMenu;
            }
            else if (e.command == "pause") {
                game1.menuHandler.currentMenu = game1.menuHandler.pauseMenu;
            }
            else if (e.command == "play") {
                game1.menuHandler.displayMenu = false;
            }
            else if (e.command == "settings") {
                game1.menuHandler.currentMenu = game1.menuHandler.settingsMenu;
            }
            else if (e.command == "quit") {
                game1.running = false;
            }
            
        }

    }

    public class ButtonEventArgs : EventArgs {

        public string command;

        public ButtonEventArgs(string command) {
            this.command = command;
        }

    }

   

    
}
