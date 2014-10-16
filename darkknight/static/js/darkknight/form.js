jQuery(function ($) {
  var $san_p = $('textarea#id_subjectAlternativeNames').closest("p"),
      san_input = '<input type="text" name="subjectAltenativeNames">';
  $san_p.find('textarea, .helptext').remove();

  $san_p.append(san_input);

  $san_p.on('keyup blur click', 'input[type="text"]', function (ev) {
    // List all the SAN domains
    var $san_inputs = $san_p.find('input[type="text"]');

    $san_inputs.each(function (idx, input) {
      var $input = $(input);

      if ($input.is(':focus')) // Don't remove the input that has the focus
        return;
      if ($input.is($san_inputs.last())) // Don't remove the last input
        return;

      if ($input.val() === '')
        $input.remove();
    });

    if ($san_inputs.last().val() !== '') {
      $san_p.append(san_input);
    }
  });
});
