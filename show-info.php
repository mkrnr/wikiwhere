<html>
  <head>
    <?php
      $new_crawl=filter_input(INPUT_GET, 'new-crawl');

      $python=filter_input(INPUT_GET, 'python');
      if (!isset($python)){
        $python="/usr/bin/python2";
      }
    ?>
  </head>
  <body>

    <?php
      $article_url = $_GET['article-url'];
      $handle = @fopen($article_url,'r');

      if($handle !== false){
         if($new_crawl == true){
           $article_json = exec($python.' get_article_data.py ' . $article_url . " " . $new_crawl);
         }else{
           $article_json = exec($python.' get_article_data.py ' . $article_url);
         }
      }
      else{
         echo "URL doesn't exist";
         return false;
      }
    ?>

    <script>
      var article_json_string = '<?php echo $article_json; ?>';
      document.write("<p>Loaded via Python, displayed via JS: </p>");
      try {
        article_json_parsed = JSON.parse(article_json_string);
      } catch (e) {
        document.write("JSON is not valid");
      }

      // print out json:
      document.write('<pre id="json"></pre>');
      document.getElementById("json").innerHTML = JSON.stringify(article_json_parsed, undefined, 2);
    </script>
  </body>
</html>
