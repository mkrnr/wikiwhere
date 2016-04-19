<html>
  <head>
    <?php
      $python=filter_input(INPUT_GET, 'python');
      if (!isset($python)){
        $python="/usr/bin/python2";
      }
    ?>
  </head>
  <body>

    <?php
      $article_url = $_POST['article-url'];
      $handle = @fopen($article_url,'r');

      if($handle !== false){
         $article_json = exec($python.' get_article_data.py ' . $article_url);
      }
      else{
         echo "URL doesn't exist";
         return false;
      }
    ?>

    <script>
      var article_json_var = "<?php echo $article_json; ?>";
      document.write("<p>loaded via python, displayed in JS: <p>")
      document.write(article_json_var)

    </script>
  </body>
</html>
