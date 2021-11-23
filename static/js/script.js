
   function generatePDF(){
     const element = document.getElementById("part_number_pdf");

     html2pdf()
     .from(element)
     .save();

   }


