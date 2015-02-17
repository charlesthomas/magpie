/* Tony O'Dell */
(function(){
  /* MODALS */
  var modals = document.getElementsByClassName("modal");
  var togglers = document.querySelectorAll("[data-toggle='modal']");
  for(var i in togglers){
    togglers[i].ontouchstart = togglers[i].onmousedown = function(){
      var id = this.getAttribute("data-modal");
      for(var i in modals){
        if(modals[i].getAttribute("id") == id){
          modals[i].className = modals[i].className.replace(/(\s|^)hidden(\s|$)/g, "");
          return;
        }
      }
    };
  }
  console.log(modals);
  console.warn(togglers);


  /* MENU STUFF */
  var drag = false;
  var divs = [document.getElementById("notebooks"), document.getElementById("notes"), document.getElementById("body")];
  var notebooks = document.getElementById("notebooks").getElementsByTagName("li");
  var notes = document.getElementById("notes").getElementsByTagName("ol");
  var open = function(e){
    if(document.body.offsetWidth >= 768){
      if(e == document.getElementById("notes") || e == document.getElementById("notebooks")){
        drag = e.onmousemove;
      }
      return 0;
    }
    for(var i in divs){
      if(divs[i].className.match(/(\s|^)slide(\s|$)/g)){
        //they're open
        return 0;
      }
      divs[i].className += " slide";
    }
    return 1;
  };
  var close = function(){
    for(var i in divs){
      divs[i].className = divs[i].className.replace(/(\s|^)slide(\s|$)/g, "");
    }
  };
  var newwidth = function(ele, eve){
    return eve.clientX - ele.offsetLeft - (ele.offsetWidth-parseInt(getComputedStyle(ele)['width']));
  };
  var setbody = function(){
    var nb = document.getElementById("notebooks");
    var n = document.getElementById("notes");
      document.getElementById("body").style.left = 
        parseInt(nb.style.width) + 
        parseInt(n.style.width) + 
        nb.offsetWidth - parseInt(getComputedStyle(nb)['width']) +
        n.offsetWidth - parseInt(getComputedStyle(n)['width']) +
        parseInt(getComputedStyle(document.getElementById("body"))['font-size']) + 
        "px";
  };
  if(localStorage){
    var notebookw = localStorage.getItem("styles_notebookpane_width");
    var notew = localStorage.getItem("styles_notepane_width");
    var nb = document.getElementById("notebooks");
    var n = document.getElementById("notes");

    if(notebookw){ 
      nb.style.width = notebookw;
      var pad = nb.offsetWidth - parseInt(getComputedStyle(nb)['width']);
      n.style.left = pad + parseInt(notebookw) + "px";
    }
    if(notew){ 
      document.getElementById("notes").style.width = notew;
    }
    setbody();
  }
  document.getElementById("search").onmousedown = function(e){ e.stopPropagation(); };
  document.body.onmouseup = window.onmouseup = function(e){
    drag = false;
  };
  document.body.onmousemove = function(e){
    if(drag){
      drag(e);
    }
  };
  document.getElementById("notes").onmousemove = function(e){
    var n = document.getElementById("notes");
    if(drag == n.onmousemove){
      var w = newwidth(n,e);
      n.style.width = w + 'px'; 
      setbody();
      if(localStorage){
        localStorage.setItem("styles_notepane_width", w + "px");
      }
    }
  };
  document.getElementById("notebooks").onmousemove = function(e){
    var nb = document.getElementById("notebooks");
    var n = document.getElementById("notes");
    if(drag == nb.onmousemove){
      var w = newwidth(nb,e);
      var pad = nb.offsetWidth - parseInt(getComputedStyle(nb)['width']) - 2;
      nb.style.width = w + 'px'; 
      n.style.left = pad + w + "px";
      setbody();
      if(localStorage){
        localStorage.setItem("styles_notebookpane_width", w + "px");
      }
    }
  };
  for(var i in divs){
    divs[i].onmouseup = function(e){ drag = false; };
    divs[i].ontouchstart = divs[i].onmousedown = function(e){
      if(!open(this)){
        close();
      }
      e.stopPropagation();
    };
  }
  for(var j in notes){
    (function(ol){
      try {
        var elems = ol.getElementsByTagName("li");
        for(var i in elems){
          try {
            if(elems[i].getAttribute("data-available") != "0"){
              elems[i].onmousedown = elems[i].ontouchstart = function(e){
                e.stopPropagation();
                if(open(this)){
                  return;
                }
                for(var i in elems){
                  try {
                    elems[i].className = elems[i].className.replace(/(\s|^)active(\s|$)/g, "");
                  } catch(e) { }
                }
                close();
                this.className += " active";
              };
            }
          } catch(e) { }
        }
      } catch(e) { }
    })(notes[j]);
  }
  for(var i in notebooks){
    try {
      if(notebooks[i].getAttribute("data-available") != "0"){
        notebooks[i].onmousedown = notebooks[i].ontouchstart = function(e){
          e.stopPropagation();
          if(open(this)){
            return;
          }
          //show the right notes
          for(var i in notes){ 
            try {
              if(notes[i].getAttribute("data-notebook") != this.getAttribute("data-id")){
                notes[i].className = notes[i].className.replace(/(\s|^)active(\s|$)/g, "");
              }else{
                if(! notes[i].className.match(/(\s|^)active(\s|$)/g)){
                  notes[i].className += " active";
                }
              }
            } catch(e) { }
          }
          for(var i in notebooks){
            try {
              notebooks[i].className = notebooks[i].className.replace(/(\s|^)active(\s|$)/g, "");
            } catch(e) { }
          }
          this.className += " active";
          var notename = "";
          var elems = document.getElementById("notes").getElementsByTagName("ol");
          for(var j in elems){
            try {
              if(elems[j].className.match(/(\s|^)active(\s|$)/g)){
                notename = elems[j].getElementsByClassName("active")[0].textContent;
              }
            } catch(e) { }
          }
        };
      }
    } catch(e) { }
  }
})();
