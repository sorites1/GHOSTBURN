document$.subscribe(function() {
  // Only target tables with the "sortable" class
  var tables = document.querySelectorAll("article table.sortable")
  tables.forEach(function(table) {
    new Tablesort(table)
  })
})