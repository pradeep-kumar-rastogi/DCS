
$(document).ready(function () {
  // Default Datatable
  $("#basic-datatable").DataTable({
    language: {
      paginate: {
        previous: "<i class='mdi mdi-chevron-left'>",
        next: "<i class='mdi mdi-chevron-right'>",
      },
    },
    drawCallback: function () {
      $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
    },
  });



// ----------------------------------sorting daa of dwonload files brand/catagory all --------------------------------------

$(document).ready(function () {
  // Set up the table object
  var table = $("#datatable-buttons4").DataTable({
    columnDefs: [
      { type: "date", targets: 0 }, // Set the sorting type as "date" for the date column
      { type: "time-ampm", targets: 4 },
      // Set the sorting type as "time-ampm" for the time column
    ],
    language: {
      paginate: {
        previous: "<i class='mdi mdi-chevron-left'>",
        next: "<i class='mdi mdi-chevron-right'>",
      },
    },
    drawCallback: function () {
      $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
    },
  });

  // Convert the time values to 24-hour format and update the table
  table.rows().every(function (rowIdx, tableLoop, rowLoop) {
    var data = this.data();
    var dateTimeStr = data[0].split(",")[1].trim(); // Extract the date and time value from the string
    var dateTimeArr = dateTimeStr.split(", "); // Split into date, time, and AM/PM
    var time = moment(dateTimeArr[1], "h:mm a").format("HH:mm"); // Convert the time to 24-hour format
    data[0] = dateTimeArr[0]; // Update the date column value
    data[1] = time; // Update the time column value
    data[2] = dateTimeArr[2]; // Update the AM/PM column value
    this.data(data); // Update the table row with the updated data array
  });

  // Trigger the sorting for the date and time columns
  table.columns([0, 1]).order(["asc", "asc"]).draw();
});



  // ----------------------------------sorting daa of upload_csv all --------------------------------------

  $(document).ready(function () {
    // Set up the table object
    var table = $("#datatable-buttons3").DataTable({
      columnDefs: [
        { type: "date", targets: 0 }, // Set the sorting type as "date" for the date column
        { type: "time-ampm", targets: 2 },
        // Set the sorting type as "time-ampm" for the time column
      ],
      language: {
        paginate: {
          previous: "<i class='mdi mdi-chevron-left'>",
          next: "<i class='mdi mdi-chevron-right'>",
        },
      },
      drawCallback: function () {
        $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
      },
    });

    // Convert the time values to 24-hour format and update the table
    table.rows().every(function (rowIdx, tableLoop, rowLoop) {
      var data = this.data();
      var dateTimeStr = data[0].split(",")[1].trim(); // Extract the date and time value from the string
      var dateTimeArr = dateTimeStr.split(", "); // Split into date, time, and AM/PM
      var time = moment(dateTimeArr[1], "h:mm a").format("HH:mm"); // Convert the time to 24-hour format
      data[0] = dateTimeArr[0]; // Update the date column value
      data[1] = time; // Update the time column value
      data[2] = dateTimeArr[2]; // Update the AM/PM column value
      this.data(data); // Update the table row with the updated data array
    });

    // Trigger the sorting for the date and time columns
    table.columns([0, 1]).order(["asc", "asc"]).draw();
  });

  // ----------------------------------sorting daa of Dashboard all --------------------------------------

  $(document).ready(function () {
    // Set up the table object
    var table = $("#datatable-buttons2").DataTable({
     
      language: {
        paginate: {
          previous: "<i class='mdi mdi-chevron-left'>",
          next: "<i class='mdi mdi-chevron-right'>",
        },
      },
      drawCallback: function () {
        $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
      },
    });
    
    $('#status-filter').on('change', function () {
      
      const selectedStatus = $(this).val();
     

      // Filter the DataTable based on the selected status
      table.column(1).search(selectedStatus).draw();
  });
 

  
  });



  // ----------------------------------sorting daa of list all --------------------------------------

  $(document).ready(function () {
    // Set up the table object
    var table = $("#datatable-buttons1").DataTable({
      columnDefs: [
        { type: "date", targets: 0 }, // Set the sorting type as "date" for the date column
        { type: "time-ampm", targets: 1 },
        // Set the sorting type as "time-ampm" for the time column
      ],
      language: {
        paginate: {
          previous: "<i class='mdi mdi-chevron-left'>",
          next: "<i class='mdi mdi-chevron-right'>",
        },
      },
      drawCallback: function () {
        $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
      },
    });

    // Convert the time values to 24-hour format and update the table
    table.rows().every(function (rowIdx, tableLoop, rowLoop) {
      var data = this.data();
      var dateTimeStr = data[0].split(",")[1].trim(); // Extract the date and time value from the string
      var dateTimeArr = dateTimeStr.split(", "); // Split into date, time, and AM/PM
      var time = moment(dateTimeArr[1], "h:mm a").format("HH:mm"); // Convert the time to 24-hour format
      data[0] = dateTimeArr[0]; // Update the date column value
      data[1] = time; // Update the time column value
      data[2] = dateTimeArr[2]; // Update the AM/PM column value
      this.data(data); // Update the table row with the updated data array
    });

    // Trigger the sorting for the date and time columns
    table.columns([0, 1]).order(["asc", "asc"]).draw();
  });

  





  // Multi Selection Datatable
  $("#selection-datatable").DataTable({
    select: {
      style: "multi",
    },
    language: {
      paginate: {
        previous: "<i class='mdi mdi-chevron-left'>",
        next: "<i class='mdi mdi-chevron-right'>",
      },
    },
    drawCallback: function () {
      $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
    },
  });

  // Key Datatable
  $("#key-datatable").DataTable({
    keys: true,
    language: {
      paginate: {
        previous: "<i class='mdi mdi-chevron-left'>",
        next: "<i class='mdi mdi-chevron-right'>",
      },
    },
    drawCallback: function () {
      $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
    },
  });

  table
    .buttons()
    .container()
    .appendTo("#datatable-buttons_wrapper .col-md-6:eq(0)");

  // Complex headers with column visibility Datatable
  $("#complex-header-datatable").DataTable({
    language: {
      paginate: {
        previous: "<i class='mdi mdi-chevron-left'>",
        next: "<i class='mdi mdi-chevron-right'>",
      },
    },
    drawCallback: function () {
      $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
    },
    columnDefs: [
      {
        visible: false,
        targets: -1,
      },
    ],
  });

  // State Datatable
  $("#state-saving-datatable").DataTable({
    stateSave: true,
    language: {
      paginate: {
        previous: "<i class='mdi mdi-chevron-left'>",
        next: "<i class='mdi mdi-chevron-right'>",
      },
    },
    drawCallback: function () {
      $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
    },
  });
});
