<!DOCTYPE html>
<html>
  <head>
    <?php
      $call="show-info.php";
      $python=filter_input(INPUT_GET, 'python');
      if (isset($python)){
        $call.="?python=".$python;
      }
    ?>
  </head>
  <body>
    <form action=<?php echo $call ?> method="get">
      Article name: <input type="text" name="article-url"><br>
      <input type="checkbox" name="new-crawl" value="true">Fresh crawl<br>
      <input type="submit">
    </form>
  </body>
</html>
