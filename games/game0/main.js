class Image {
  constructor(x, y,  width, height, image_src) {
    this.Image = document.createElement('img');
    this.Image.style.width = width;
    this.Image.style.height = height;
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
      if (this.shouldMove) {
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
        }}
    }, 16);
  }

  startMovement() {
    this.shouldMove = true;
  }

  stopMovement(direction) {
    this.shouldMove=false;
  }

  display() {
    this.Image.style.display = "block";
  }

  hide() {
    this.Image.style.display = "none";
  }
  
};

let img1 = new Image(100, 100, 50, 50, 'img1.webp');
img1.display();
let img2 = new Image(300, 300, 'auto', 'auto', 'img2.png');
img2.display();
let img3 = new Image(0, 0, 'auto', 'auto', 'img1.webp');
img3.startMovement();
img3.display();
