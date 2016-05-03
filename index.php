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
      Article URL: <input type="text" name="article-url" size=50 placeholder="https://de.wikipedia.org/wiki/Test"><br>
      <input type="checkbox" name="new-crawl" value="true">Fresh crawl<br>
      <input type="submit">
    </form>
  </body>
</html>
