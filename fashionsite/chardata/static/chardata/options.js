function optionsBooleanToYesNo(bool_param) {
    return (bool_param) ? 'yes' : 'no';
}

function optionsBooleanGelanoToYesNo(bool_param) {
    if (bool_param === 'gelano') {
        return 'gelano'
    }
    return (bool_param) ? 'yes' : 'no';
}

function optionsBooleanTrophiesToYesNo(bool_param) {
    if (bool_param === 'lightset') {
        return 'lightset'
    }
    if (bool_param === 'cawwot') {
        return 'cawwot'
    }
    return (bool_param) ? 'yes' : 'no';
}

function optionsInit(options, prysmaradites) {
    var $apExoRadios = $('input:radio[name=ap_exo]');
    $apExoRadios.filter('[value=' + optionsBooleanToYesNo(options['ap_exo']) + ']')
        .prop('checked', true);
        
    var $rangeExoRadios = $('input:radio[name=range_exo]');
    $rangeExoRadios.filter('[value=' + optionsBooleanToYesNo(options['range_exo']) + ']')
        .prop('checked', true);

    var $mpExoRadios = $('input:radio[name=mp_exo]');
    $mpExoRadios.filter('[value=' + optionsBooleanGelanoToYesNo(options['mp_exo']) + ']')
        .prop('checked', true);
        
    var $rhineetleCheckbox = $('input:checkbox[name=rhineetle]');
    $rhineetleCheckbox.prop('checked', options.rhineetle);
    
    var $dragoturkeyCheckbox = $('input:checkbox[name=dragoturkey]');
    $dragoturkeyCheckbox.prop('checked', options.dragoturkey);
    
    var $seemyoolCheckbox = $('input:checkbox[name=seemyool]');
    $seemyoolCheckbox.prop('checked', options.seemyool);
    
    var $dofusRadios = $('input:radio[name=dofus]');
    $dofusRadios.filter('[value=' + optionsBooleanTrophiesToYesNo(options['dofus']) + ']')
        .prop('checked', true);
        
    var $ochreCheckbox = $('input:checkbox[name=ochre]');
    $ochreCheckbox.prop('checked', options.dofuses.ochre);
    
    var $vulbisCheckbox = $('input:checkbox[name=vulbis]');
    $vulbisCheckbox.prop('checked', options.dofuses.vulbis);
    
    var $dolmanaxCheckbox = $('input:checkbox[name=dolmanax]');
    $dolmanaxCheckbox.prop('checked', options.dofuses.dolmanax);
    
    var $iceCheckbox = $('input:checkbox[name=ice]');
    $iceCheckbox.prop('checked', options.dofuses.ice);
    
    var $crimsonCheckbox = $('input:checkbox[name=crimson]');
    $crimsonCheckbox.prop('checked', options.dofuses.crimson);
    
    var $emeraldCheckbox = $('input:checkbox[name=emerald]');
    $emeraldCheckbox.prop('checked', options.dofuses.emerald);
    
    var $cawwotCheckbox = $('input:checkbox[name=cawwot]');
    $cawwotCheckbox.prop('checked', options.dofuses.cawwot);
    
    var $dokokoCheckbox = $('input:checkbox[name=dokoko]');
    $dokokoCheckbox.prop('checked', options.dofuses.dokoko);
    
    var $ivoryCheckbox = $('input:checkbox[name=ivory]');
    $ivoryCheckbox.prop('checked', options.dofuses.ivory);
    
    var $watchersCheckbox = $('input:checkbox[name=watchers]');
    $watchersCheckbox.prop('checked', options.dofuses.watchers);
    
    var $cloudyCheckbox = $('input:checkbox[name=cloudy]');
    $cloudyCheckbox.prop('checked', options.dofuses.cloudy);
    
    var $turquoiseCheckbox = $('input:checkbox[name=turquoise]');
    $turquoiseCheckbox.prop('checked', options.dofuses.turquoise);
    
    var $dotrichCheckbox = $('input:checkbox[name=dotrich]');
    $dotrichCheckbox.prop('checked', options.dofuses.dotrich);
    
    var $kaliptusCheckbox = $('input:checkbox[name=kaliptus]');
    $kaliptusCheckbox.prop('checked', options.dofuses.kaliptus);
    
    var $grofusCheckbox = $('input:checkbox[name=grofus]');
    $grofusCheckbox.prop('checked', options.dofuses.grofus);
    
    var $abyssalCheckbox = $('input:checkbox[name=abyssal]');
    $abyssalCheckbox.prop('checked', options.dofuses.abyssal);
    
    var $lavasmithCheckbox = $('input:checkbox[name=lavasmith]');
    $lavasmithCheckbox.prop('checked', options.dofuses.lavasmith);

    var $blackspottedCheckbox = $('input:checkbox[name=blackspotted]');
    $blackspottedCheckbox.prop('checked', options.dofuses.blackspotted);
    
    var $ebonyCheckbox = $('input:checkbox[name=ebony]');
    $ebonyCheckbox.prop('checked', options.dofuses.ebony);

    var $silverCheckbox = $('input:checkbox[name=silver]');
    $silverCheckbox.prop('checked', options.dofuses.silver);

    var $sparklingsilverCheckbox = $('input:checkbox[name=sparklingsilver]');
    $sparklingsilverCheckbox.prop('checked', options.dofuses.sparklingsilver);

    var $cocoaCheckbox = $('input:checkbox[name=cocoa]');
    $cocoaCheckbox.prop('checked', options.dofuses.cocoa);

    var $domakuroCheckbox = $('input:checkbox[name=domakuro]');
    $domakuroCheckbox.prop('checked', options.dofuses.domakuro);

    var $dorigamiCheckbox = $('input:checkbox[name=dorigami]');
    $dorigamiCheckbox.prop('checked', options.dofuses.dorigami);

    var $nightmareCheckbox = $('input:checkbox[name=nightmare]');
    $nightmareCheckbox.prop('checked', options.dofuses.nightmare);    var $sylvanCheckbox = $('input:checkbox[name=sylvan]');
    $sylvanCheckbox.prop('checked', options.dofuses.sylvan);

    // Initialize individual prysmaradite checkboxes
    if (prysmaradites && prysmaradites.prysmaradites) {
        // Prytekt family
        var $prytektCheckbox = $('input:checkbox[name=prytekt]');
        $prytektCheckbox.prop('checked', prysmaradites.prysmaradites.prytekt);
        
        var $shinyPrytektCheckbox = $('input:checkbox[name=shiny_prytekt]');
        $shinyPrytektCheckbox.prop('checked', prysmaradites.prysmaradites.shiny_prytekt);
        
        var $iridescentPrytektCheckbox = $('input:checkbox[name=iridescent_prytekt]');
        $iridescentPrytektCheckbox.prop('checked', prysmaradites.prysmaradites.iridescent_prytekt);
        
        // Pryssure family
        var $pryssureCheckbox = $('input:checkbox[name=pryssure]');
        $pryssureCheckbox.prop('checked', prysmaradites.prysmaradites.pryssure);
        
        var $shinyPryssureCheckbox = $('input:checkbox[name=shiny_pryssure]');
        $shinyPryssureCheckbox.prop('checked', prysmaradites.prysmaradites.shiny_pryssure);
        
        var $iridescentPryssureCheckbox = $('input:checkbox[name=iridescent_pryssure]');
        $iridescentPryssureCheckbox.prop('checked', prysmaradites.prysmaradites.iridescent_pryssure);
        
        // Surpryz family
        var $surpryzCheckbox = $('input:checkbox[name=surpryz]');
        $surpryzCheckbox.prop('checked', prysmaradites.prysmaradites.surpryz);
        
        var $shinySurpryzCheckbox = $('input:checkbox[name=shiny_surpryz]');
        $shinySurpryzCheckbox.prop('checked', prysmaradites.prysmaradites.shiny_surpryz);
        
        var $iridescentSurpryzCheckbox = $('input:checkbox[name=iridescent_surpryz]');
        $iridescentSurpryzCheckbox.prop('checked', prysmaradites.prysmaradites.iridescent_surpryz);
        
        // Pryndsight family
        var $pryndsightCheckbox = $('input:checkbox[name=pryndsight]');
        $pryndsightCheckbox.prop('checked', prysmaradites.prysmaradites.pryndsight);
        
        var $shinyPryndsightCheckbox = $('input:checkbox[name=shiny_pryndsight]');
        $shinyPryndsightCheckbox.prop('checked', prysmaradites.prysmaradites.shiny_pryndsight);
        
        var $iridescentPryndsightCheckbox = $('input:checkbox[name=iridescent_pryndsight]');
        $iridescentPryndsightCheckbox.prop('checked', prysmaradites.prysmaradites.iridescent_pryndsight);
        
        // Prylixir family
        var $prylixirCheckbox = $('input:checkbox[name=prylixir]');
        $prylixirCheckbox.prop('checked', prysmaradites.prysmaradites.prylixir);
        
        var $shinyPrylixirCheckbox = $('input:checkbox[name=shiny_prylixir]');
        $shinyPrylixirCheckbox.prop('checked', prysmaradites.prysmaradites.shiny_prylixir);
        
        var $iridescentPrylixirCheckbox = $('input:checkbox[name=iridescent_prylixir]');
        $iridescentPrylixirCheckbox.prop('checked', prysmaradites.prysmaradites.iridescent_prylixir);
        
        // Pryveil family
        var $pryveilCheckbox = $('input:checkbox[name=pryveil]');
        $pryveilCheckbox.prop('checked', prysmaradites.prysmaradites.pryveil);
        
        var $shinyPryveilCheckbox = $('input:checkbox[name=shiny_pryveil]');
        $shinyPryveilCheckbox.prop('checked', prysmaradites.prysmaradites.shiny_pryveil);
        
        var $iridescentPryveilCheckbox = $('input:checkbox[name=iridescent_pryveil]');
        $iridescentPryveilCheckbox.prop('checked', prysmaradites.prysmaradites.iridescent_pryveil);
    }
}

function disableUnusableDofus(unusable){
    for (var key in unusable){
        var classStr = ".".concat(key);
        $(classStr).attr('disabled',true);
        $(classStr).attr('checked',false);
        $(classStr).css({ 'opacity' : 0.7 });
        $(classStr).attr('title', gettext('You need to be a higher level to equip this Dofus'));
    }
}

function disableUnusablePrysmaradites(unusable){
    for (var key in unusable){
        var classStr = ".".concat(key);
        $(classStr).attr('disabled',true);
        $(classStr).attr('checked',false);
        $(classStr).css({ 'opacity' : 0.7 });
        $(classStr).attr('title', gettext('You need to be a higher level to equip this Prysmaradite'));
    }
}

