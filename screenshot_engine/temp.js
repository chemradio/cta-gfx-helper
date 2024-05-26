var redColor = [0.98431372642517, 0.00784313771874, 0.16470588743687, 1];
var blueColor = [0.00784313771874, 0.16470588743687, 0.98431372642517, 1];
var whiteColor = [1, 1, 1, 1];
var blackColor = [0, 0, 0, 1];
var check = thisComp.layer("control").effect("Color Theme")("Menu");

if (check == 1) {
  redColor;
} else if (check == 2) {
  blueColor;
} else if (check == 3) {
  whiteColor;
} else if (check == 4) {
  blackColor;
}
