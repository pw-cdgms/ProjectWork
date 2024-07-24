if (window.addEventListener) // W3C standard
{
  window.addEventListener('load', animate, false); // NB **not** 'onload'
} 
else if (window.attachEvent) // Microsoft
{
  window.attachEvent('onload', animate);
}

var delta = 800;
var forwardDelta = 100;
var backwardDetla = 75;
var switchDelta = 800;

function animate() {
    var element = document.getElementsByClassName("textData")[0];
    var elementData = JSON.parse(element.getAttribute("data-to-animate"));
    var originalText = element.innerText;
    moveLetters(element, originalText, elementData, 0, 0, true);
}

function moveLetters(element, originalText, elementData, elementDataIndex, currentDataIndex, directionForwards) {
    switchDirection = false;
    updateText(element, originalText + elementData[elementDataIndex].substring(0, currentDataIndex));
    nextIndex = -1;
    delta = 0;
    if(directionForwards) {
        if(currentDataIndex == elementData[elementDataIndex].length) {
            nextIndex = elementData[elementDataIndex].length - 1;
            directionForwards = !directionForwards;
            delta = switchDelta;
            if(elementDataIndex == elementData.length - 1) {
                setTimeout(() => {
                    animateShrug();
                }, 500);
                return;
            }
        }
        else {
            nextIndex = currentDataIndex + 1;
            delta = forwardDelta;
        }
    }
    else {
        if(currentDataIndex == 0) {
            nextIndex = 0;
            directionForwards = !directionForwards;
            delta = switchDelta;
            elementDataIndex = elementDataIndex + 1;
        }
        else {
            nextIndex = currentDataIndex - 1;
            delta = backwardDetla;
        }
    }

    setTimeout(() => {
        moveLetters(element, originalText, elementData, elementDataIndex, nextIndex, directionForwards);
    }, delta);
}

function updateText(element, text) {
    element.innerText = text;
}

function animateShrug() {

    document.getElementById("leftArm").style.animation = "leftarm 3s";
    document.getElementById("leftArm").style.WebkitAnimation = "leftarm 3s";
    document.getElementById("rightArm").style.animation = "rightarm 3s";
    document.getElementById("rightArm").style.WebkitAnimation = "rightarm 3s";

}