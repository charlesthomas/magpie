$("*[contenteditable='true']").hallo({
  plugins: {
    'halloformat': {},
    'halloblock': {},
    'hallojustify': {},
    'hallolists': {},
    //'hallolink': {},
    'halloreundo': {}
  },
  editable: true,
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
  if (markdownize($("*[contenteditable='true']").html()) == content) {
    return;
  }
  var html = htmlize(content);
  $("*[contenteditable='true']").html(html); 
};

$("*[contenteditable='true']").bind('hallomodified', function(event, data) {
  showSource(data.content);
});
updateHtml($("textarea").html());
