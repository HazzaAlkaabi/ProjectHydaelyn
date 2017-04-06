using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace Game1 {

    public class Camera {

        public Vector2 pos;
        public float zoom;
        public Vector2 resolution;

        public Camera(Vector2 resolution,  Vector2 pos, float zoom) {
            this.pos = pos;
            this.zoom = zoom;
            this.resolution = resolution;
        }

        Vector2 gamePosToScreenPos(Vector2 gamePos) {
            // Convert game positions to screen positions for rendering
            float posX = ((gamePos.X - this.pos.X) * this.zoom) + (this.resolution.X / 2) * (1 - this.zoom);
            float posY = ((gamePos.Y - this.pos.Y) * this.zoom) + (this.resolution.Y / 2) * (1 - this.zoom);
            Vector2 screenPos = new Vector2(posX, posY);

            return screenPos;
        }

        Vector2 screenPosToGamePos(Vector2 screenPos) {
            // Convert screen positions to game positions for player interactions
            // Not sure if correct
            float posX = ((this.pos.X - (this.resolution.X / 2) * (1 - this.zoom)) / this.zoom) + this.pos.X;
            float posY = ((this.pos.Y - (this.resolution.Y / 2) * (1 - this.zoom)) / this.zoom) + this.pos.Y;
            Vector2 gamePos = new Vector2(posX, posY);
            return gamePos;
        }
    }
}
