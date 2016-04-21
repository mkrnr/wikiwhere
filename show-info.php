<!DOCTYPE html>
<html>
  <head>
    <?php
      $new_crawl=filter_input(INPUT_GET, 'new-crawl');

      $python=filter_input(INPUT_GET, 'python');
      if (!isset($python)){
        $python="/usr/bin/python2";
      }
    ?>
	<script type="text/javascript" src="js/d3.js"></script>
  </head>
  <body>

    <?php
      $article_url = $_GET['article-url'];
      $handle = @fopen($article_url,'r');

      if($handle !== false){
         if($new_crawl == true){
           $article_path = exec($python.' get_article_data.py ' . $article_url . " " . $new_crawl);
         }else{
           $article_path = exec($python.' get_article_data.py ' . $article_url);
         }
      }
      else{
         echo "URL doesn't exist";
         return false;
      }
    ?>
	<div id="datatable"></div>
	<script>
	  var article_path = '<?php echo $article_path; ?>';
	  d3.json('<?php echo $article_path; ?>', function (error, data){
		  function tabulate(data, columns) {
			var table = d3.select('body').append('table')
			var thead = table.append('thead')
			var	tbody = table.append('tbody');

		// append the header row
		thead.append('tr')
		  .selectAll('th')
		  .data(columns).enter()
		  .append('th')
		    .text(function (column) { return column.id; });

		// create a row for each object in the data
		var rows = tbody.selectAll('tr')
		  .data(data.objects)
		  .enter()
		  .append('tr');

		// create a cell in each row for each column
		var cells = rows.selectAll('td')
		  .data(function (row) {
		    return columns.map(function (column) {
		      return {column: column.id, value: eval('row.'+column.key) };
		    });
		  })
		  .enter()
		  .append('td')
		    .text(function (d) { return d.value; });

	  return table;
	}

	// render the table(s)
	tabulate(data, ['classification', 'classification-general']); // 2 column table

		  });
	</script>
    <script>
      var article_path = '<?php echo $article_path; ?>';
      //document.write("<p>Loaded via Python, displayed via JS: </p>");
      //try {
      //  article_json_parsed = JSON.parse(article_json_string);
      //} catch (e) {
      //  document.write("JSON is not valid");
      //}
      document.write(article_path);

      // print out json:
      document.write('<pre id="json"></pre>');
      document.getElementById("json").innerHTML = JSON.stringify(article_json_parsed, undefined, 2);
    </script>
  </body>
</html>
