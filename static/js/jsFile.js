/*
===============================================================

Hi! Welcome to my little playground!

My name is Tobias Bogliolo. 'Open source' by default and always 'responsive',
I'm a publicist, visual designer and frontend developer based in Barcelona. 

Here you will find some of my personal experiments. Sometimes usefull,
sometimes simply for fun. You are free to use them for whatever you want 
but I would appreciate an attribution from my work. I hope you enjoy it.

===============================================================
*/

$(document).ready(function(){
    //Show contextmenu:
    $('.items').contextmenu(function(e){
      // var item = $(this).text()
      var item = $(this).text()
      allPath = $(location).attr('pathname')
      host = $(location).attr('host')
      
      var context = $('.contextmenu li a')
      // console.log(allPath.split("/"))

      // console.log(allPath)
      allPathArry = allPath.split("/")
      needPath1 = allPathArry.splice(1, 2).join('/')
      needPath2 = allPathArry.splice(2, allPathArry.length-2).join('/')

      // console.log(needPath2)
      
      // console.log(allPathArry.length)
      // console.log("needPath: ",needPath1 + " and " + needPath2)
      
      // console.log("temp: ", temp)
      // console.log("http://" + host + needPath1 +"/delete" + needPath2 + item)
      // console.log(host + "/delete" + allPath + item )
      context[0].href = "http://" + host + '/' + needPath1 +"/delete/" + needPath2 +'/' + item
      context[1].href = "http://" + host + '/' + needPath1 +"/move/" + needPath2 +'/' + item
      context[2].href = "http://" + host + '/' + needPath1 +"/log/" + needPath2 +'/' + item
      //Get window size:
      var winWidth = $(document).width();
      var winHeight = $(document).height();
      //Get pointer position:
      var posX = e.pageX;
      var posY = e.pageY;
      //Get contextmenu size:
      var menuWidth = $(".contextmenu").width();
      var menuHeight = $(".contextmenu").height();
      //Security margin:
      var secMargin = 10;
      //Prevent page overflow:
      if(posX + menuWidth + secMargin >= winWidth
      && posY + menuHeight + secMargin >= winHeight){
        //Case 1: right-bottom overflow:
        posLeft = posX - menuWidth - secMargin + "px";
        posTop = posY - menuHeight - secMargin + "px";
      }
      else if(posX + menuWidth + secMargin >= winWidth){
        //Case 2: right overflow:
        posLeft = posX - menuWidth - secMargin + "px";
        posTop = posY + secMargin + "px";
      }
      else if(posY + menuHeight + secMargin >= winHeight){
        //Case 3: bottom overflow:
        posLeft = posX + secMargin + "px";
        posTop = posY - menuHeight - secMargin + "px";
      }
      else {
        //Case 4: default values:
        posLeft = posX + secMargin + "px";
        posTop = posY + secMargin + "px";
      };
      //Display contextmenu:
      $(".contextmenu").css({
        "left": posLeft,
        "top": posTop
      }).show();
      //Prevent browser default contextmenu.

      return false;
    });
    //Hide contextmenu:
    $(document).click(function(){
      $(".contextmenu").hide();
    });
  });