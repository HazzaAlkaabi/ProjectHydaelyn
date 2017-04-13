using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace KeyboardEvents {



    public delegate void KeyboardEventHandler(Object sender, KeyboardEventArgs args);


    public static class KeyboardEvents {

        static public MainGame.Game1 game1;

        static public void changeMenu(Object sender, KeyboardEventArgs e) {

            // if (e.command == "something"){
            // do something
            //}

        }

    }

    public class KeyboardEventArgs : EventArgs {

        public string command;

        public KeyboardEventArgs(string command) {
            this.command = command;
        }

    }


}
