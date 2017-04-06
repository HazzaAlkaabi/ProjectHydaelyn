using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Game1;
using Menus;

namespace Events {



    static class EventHandler {

        static public Game1.Game1 game1;

        static public void changeMenu(Object sender, EventArgs args) {
            System.Console.WriteLine("Click");
            game1.menuHandler.currentMenu = game1.menuHandler.pauseMenu;
            
        }

    }

   

    
}
