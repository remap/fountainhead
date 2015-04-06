/**
 * Script control Javascript containing UI control functions.
 */

/**
 * Toggle 'display' in plain JS by class name
 *
 * Note: Difference between display and visibility: a hidden element is still taking up the space
 * while a 'none' display element is not; Implementing the function as 'display:none' for now.
 */
function toggleClassVisibility(className, visible)
{
  var flag = visible;
  var elements = document.getElementsByClassName(className);
  
  if (elements == undefined || elements.length == 0) {
    console.log("No elements of such class " + className);
    return ;
  }
  
  if (flag == undefined) {
    flag = elements[0].style.display;
  }
  
  if (flag != 'none' || flag == false) {
    flag = 'none';
  } else if (flag == 'none' || flag == true) {
    flag = 'inline';
  } else {
    console.log("Unrecognized toggle flag option: " + flag);
  }
  
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.display = flag;
  }
}

/*
window.onload = function() {
  toggleClassVisibility('dialogue');
}
*/