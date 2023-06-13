class Image {
  constructor(width = "auto", height = "auto", x, y, image_src) {
    this.Image = document.createElement('img');
    this.Image.width = width;
    this.Image.height = height;
    this.Image.style.position = "absolute";
    this.Image.style.left = x + "px";
    this.Image.style.top = y + "px";
    this.Image.src = image_src;

    // Set initial display style property to "none"
    this.Image.style.display = "none";

    // Add the image element to the document body
    document.body.appendChild(this.Image);

    // Set initial movement values
    this.directions = {};

    // Add event listeners for arrow key movement
    document.addEventListener("keydown", (event) => {
      switch (event.key) {
        case "ArrowLeft":
        case "a":
          this.directions.left = true;
          break;
        case "ArrowRight":
        case "d":
          this.directions.right = true;
          break;
        case "ArrowUp":
        case "w":
          this.directions.up = true;
          break;
        case "ArrowDown":
        case "s":
          this.directions.down = true;
          break;
      }
    });

    document.addEventListener("keyup", (event) => {
      switch (event.key) {
        case "ArrowLeft":
        case "a":
          this.directions.left = false;
          break;
        case "ArrowRight":
        case "d":
          this.directions.right = false;
          break;
        case "ArrowUp":
        case "w":
          this.directions.up = false;
          break;
        case "ArrowDown":
        case "s":
          this.directions.down = false;
          break;
      }
    });

    // Update the image position every 16 milliseconds (60 frames per second)
    setInterval(() => {
      if (this.directions.left) {
        this.Image.style.left = parseInt(this.Image.style.left) - 1 + "px";
      }
      if (this.directions.right) {
        this.Image.style.left = parseInt(this.Image.style.left) + 1 + "px";
      }
      if (this.directions.up) {
        this.Image.style.top = parseInt(this.Image.style.top) - 1 + "px";
      }
      if (this.directions.down) {
        this.Image.style.top = parseInt(this.Image.style.top) + 1 + "px";
      }
    }, 16);
  }

  startMovement(direction) {
    this.directions[direction] = true;
  }

  stopMovement(direction) {
    this.directions[direction] = false;
  }

  display() {
    this.Image.style.display = "block";
  }

  hide() {
    this.Image.style.display = "none";
  }
}

let img1 = new Image(50, 50, 100, 100, 'img1.webp');
let img2 = new Image(100, 100, 300, 300, 'img2.png');
img1.display();
img2.display();