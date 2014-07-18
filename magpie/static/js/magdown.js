$(document).ready(function(){
  $(".editable").hallo({
    plugins: {
      'halloformat': {},
      'halloblock': {},
      'hallojustify': {},
      'hallolists': {},
      'halloreundo': {}
    },
    editable: true,
    toolbar: "halloToolbarFixed"
  });

  var markdownize = function(content) {
    var html = content.split("\n").map($.trim).filter(function(line) { 
      return line != "";
    }).join("\n");
    return toMarkdown(html);
  };
  var converter = new Showdown.converter();
  var htmlize = function(content) {
    return converter.makeHtml(content);
  };

  var showSource = function(content) {
    var markdown = markdownize(content);
    if($("textarea").get(0).value == markdown){
      return;
    }
    $("textarea").get(0).value = markdown;
  };

  var updateHtml = function(content) {
    if (markdownize($(".editable").html()) == content) {
      return;
    }
    var html = htmlize(content);
    $(".editable").html(html); 
  };

  $(".editable").bind('hallomodified', function(event, data) {
    showSource(data.content);
  });
  updateHtml($("textarea").html());

/*
  $("*").swipe({
    swipe: function(e,dir){
      if(dir === "left"){
        $(".row-offcanvas").removeClass("active");
      }else if($(".visible-xs").is(":visible") && dir === "right"){
        $(".row-offcanvas").addClass("active");
      }
    }
    ,threshold: 38
  });
*/

});
