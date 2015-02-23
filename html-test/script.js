function add_class (search, replacement) {
    var all = document.getElementsByTagName("*");
    for (var i=0, max=all.length; i < max; i++) {
         var text = all[i].textContent || all[i].innerText;
         if (text.indexOf(search) !== -1 && ! all[i].hasChildNodes()) {
            all[i].className = all[i].className + " " + replacement;
         }
    }
}

var replacements = [
    ["Twitter","twitter"],
    //
]

for (var i = replacements.length - 1; i >= 0; i--) {
    add_class(replacements[i][0],replacements[i][1]);
};