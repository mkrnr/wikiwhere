<!DOCTYPE html>
<html>
  <head>
    <?php
      $default="https://de.wikipedia.org/wiki/Krimkrise";
      $call="show-info.php";
      $python=filter_input(INPUT_GET, 'python');
      if (isset($python)){
        $call.="?python=".$python;
      }
    ?>
      
  </head>
  <body>
    <form action=<?php echo $call ?> method="get">
      Article URL: <input type="text" id="article-input" name="article-url" size=50 placeholder=<?php echo $default; ?>><br>
      <input type="checkbox" name="new-crawl" value="true">Fresh crawl<br>
      <input type="submit">
    </form>
    <script type="text/javascript">
      document.getElementById('article-input').value = "<?php echo $default; ?>";
    </script>
  </body>
</html>
