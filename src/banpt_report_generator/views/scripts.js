var banpt_collapseReportTablesTabsInterval;

var banpt_collapseReportTablesTabs = function (tabs) {
  var tabsHtml = tabs.html();
  tabs.replaceWith(
    '<hr /> \
    <div class="dropdown" id="banpt_report_tables_menu_container"> \
      <a class="btn dropdown-toggle banpt_report_tables_menu" data-toggle="dropdown" href="#"> \
        <span class="banpt_report_tables_menu_text">Pilih tabel</span> \
        <span class="caret"></span> \
      </a> \
      <ul class="dropdown-menu banpt_report_tables_dropdown" role="tablist"></ul> \
    </div>'
  );
  
  var dropdown = $('.banpt_report_tables_dropdown');
  dropdown.append(tabsHtml);

  // Clear all active classes as it won't be cleared automatically due to the HTML changes
  dropdown.find('li > a').parent().removeClass('active');

  // Clear all active classes on tab change as it won't be cleared automatically due to the HTML changes
  dropdown.find('li > a').on('shown.bs.tab', function () {
    console.log($(this).parent().get(0));
    $(this).parent().removeClass('active');
  });
}

$(document).ready(function () {
  banpt_collapseReportTablesTabsInterval = setInterval(function () {
    var tabs = $('.banpt_report_tables .o_notebook ul.nav.nav-tabs');
    if (tabs.html()) {
      clearInterval(banpt_collapseReportTablesTabsInterval);
      banpt_collapseReportTablesTabs(tabs);
    }
  }, 500);
});
