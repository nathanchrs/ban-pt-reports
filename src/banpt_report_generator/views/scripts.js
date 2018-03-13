
$(document).ready(function () {
  setInterval(function () {
    // Clear all active classes on tab change as it won't be cleared automatically due to the HTML changes
    var tabs = $('.banpt_report_tables_dropdown a[data-toggle="tab"]');
    tabs.parent().removeClass('active');
    tabs.off('shown.bs.tab');
    tabs.on('shown.bs.tab', function (e) {
      $(e.target).parent().removeClass('active');
    });
  }, 5000);
});
