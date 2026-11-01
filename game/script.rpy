## Sea's Company
## Adapted from "Sea's Company (Structured).docx".
##
## Notes on the source conventions (from the document's comments):
## - "Scene bg X" clears the screen and shows a background.
## - "Narr" is the narrator. "Stan (A Voice)" shows an alternate name while the
##   code still knows that Stan is speaking (see s_voice and s_beanie).
## - "Branch" is a menu. Its options can split the story into different
##   timelines; play returns afterward unless a branch jumps elsewhere.
## - "repeat branch" repeats the menu without the option just chosen. That is
##   done with a menu set.
## - Text in {curly braces} goes in the "action bubble" next to the speaker's
##   name. Here that is the show_act argument.
## - "$x += 2" changes approval; approve() also notifies the player.


label start:

    jump rescue


################################################################################
## Rescue
################################################################################

label rescue:

    scene black
    call chapter(_("Rescue"), _("Somewhere in the North Atlantic"))

    scene bg raft at heat
    show sun_glare
    with slowfade

    "Nothing but dark water as far as the eye can see. The sun beats mercilessly upon your dehydrated body, sprawled as it is across a flotilla of plastic garbage and styrofoam chunks."
    "You've long since lost the ability to raise your head to scan the horizon for rescue. You pull your hat down further over your face, resigned to your fate."

    "Your small raft is jostled by waves. Vaguely, you register a roaring motor assaulting your ears, but after days of silence you assume it's your own parched brain screaming at itself."
    "You lack the energy to care. Your every nerve and sinew ache with dusty, creaking pain."

    with vpunch
    s_voice "Whoa, there's a body on this thing! Sixer, reverse engines!"

    s_voice "Hey! You alive down there?"

    "You don't know if this is just another hallucination, but the smell of exhaust smoke ignites something inside you and you do your best to raise your arm in a limp wave."

    s_voice "They're alive! Sixer, full stop!"

    "You feel your limp body yanked upright by a strong pair of arms before succumbing to the darkness."

    scene black with blackout
    pause 1.0

    "You flounder toward consciousness with a vague, fever-dream recollection of someone holding a cup to your lips as you drank water, and then later on some kind of rich broth."
    "You reach out weakly and encounter only soft blankets. You can still feel the gentle roll of the ocean."

    scene bg bunk at wake

    "When your eyes open, you find yourself alone in a claustrophobic, closet-sized room. You can hear the lapping of waves, the deep hum of a motor, and the murmur of a conversation somewhere outside."
    "One of the voices raises a bit and you can just make out a word, \"{b}...Reykjavik!{/b}\" before it recedes into the ambient soundscape."

    p "Reykjavik? {i}ICELAND??{/i} {b}That's impossible!{/b} How long was I drifting out there?"

    "You raise your head slowly and grit your teeth until it stops spinning. Your roaming eyes catch sight of a small bottle of water within reach. Grabbing it, you gulp it greedily, water spilling over your bare chest."

    p "What the... where are my clothes?!"

    "Your skin feels clean of the itchy brine and sweat that you remember last, and the parts of you that had blistered in the relentless sun have been treated and bandaged."
    "Wherever you are, it seems you're safer than you were last time you were lucid, at least, but this doesn't really look like an official rescue vessel."

    "Hanging from above is what looks like a bag of saline and the cords of an IV, and when you scan your arms you note a small bandage in the crook of your right elbow, indicating that you were previously administered intravenous fluids."
    "Considering how much better you feel, you're grateful, if still a little unnerved by the thought of someone poking you with needles while you were unconscious."

    $ bunk_menu = set()

    menu bunk_branch:
        set bunk_menu

        "(Call out)":
            p "Um... hello?"
            "Your voice is rough with dehydration and lack of use, but the distant murmuring stops and you can hear approaching footsteps."

        "(Look around)":
            "The space is small enough that if you leaned far enough out of the bunk, you could touch the far wall."
            "There are photos and drawings stuck to the wall showing various people and places, but predominantly featuring a smiling pair of youngsters; a boy and girl with matching auburn hair."
            "Some dirty laundry is evident on the floor along with a pair of old slippers. A dog-eared paperback romance novel sits in the corner of the bed."
            jump bunk_branch

        "(Get up)":
            show bg bunk dark with Dissolve(0.4)
            "In the attempt to sit up, you faint again."
            scene black with dissolve
            "As you collapse back into the bunk you vaguely hope that when you open your eyes you'll see a kind old wizard who is ready to tell you where and when you are and what the heck is happening, and why you've been chosen for this glorious quest."
            "..."
            scene bg bunk at wake
            "...no such luck."
            jump bunk_branch

    show stan neutral at left
    show ford neutral at right

    "A cool blast of air startles your eyes open (when had you closed them?) as two tall, identical men enter the tight space."
    "Squinting at them, you note that despite their matching faces and anoraks, one of them is slightly broader and wearing a red woolen beanie, while the other has a defined cleft in his chin and is sporting a windblown mane of silver-streaked hair."
    "Both have identical expressions of concern on their square-jawed faces."

    s_beanie "Hey kid, you're finally awake!"

    show stan smile at left

    "Beanie Guy chuckles to himself as Cleft Chin guy shines a small pen-light into your eyes and grasps your wrist for a moment, taking your pulse before noticing the empty cup by the bedside."

    f_cleft "Ah, you found the water, good. You were abysmally dehydrated. I highly doubt you would've made it another day out there."

    "His tone and posture give you the nagging feeling that your predicament was somehow your own fault. You wonder if that's true."

    show ford frown at right

    menu:

        "Thank them.":
            p "I thought so, too. I owe you my life. Thank you for..."
            p "{i}...{/i}" (show_act=_("you gesture weakly to your pitiful body and its surroundings"))
            p "...all this."
            "Both men blush and smile."
            show stan uncomfortable
            show ford uncomfortable
            s_beanie "Hey, no problem. I'm just glad we got to you in time."
            $ approve("stan", 2)
            $ approve("ford", 2)

        "Voice your concerns.":
            p "What's the eye exam for, and did you {i}undress me{/i}?"
            "Both men blush and look a bit uncomfortable."
            show stan uncomfortable
            show ford uncomfortable
            f_cleft "It was that or allow you to succumb to hypothermia. You were soaked through and your temperature was well below safe levels, requiring us to raise your temperature by putting you under the hot shower for quite a while."
            p "You SHOWERED with me while I was unconscious??"
            s_beanie blush "I just propped you up against the wall. It was too steamy to see anything in there, honest!"
            p "Riiiiight."
            f_cleft frown "It was that or let your vital organs shut down."
            p "Okay, fine, that probably makes sense."

        "Bust out in laughter, hurting your dry throat.":
            p "Oh for cripes sake, I can't believe I've become a meme!"
            show stan laugh at left, hop
            s_beanie grin "See, Sixer! EVERYBODY knows that joke!"
            $ approve("stan", 2)

    show ford neutral
    show stan neutral

    "Cleft Chin picks up a bundle from a nearby shelf and leans toward you."

    f_cleft "Your clothes have been laundered and are currently drying. In the meantime you can borrow these."

    "He places a pile of what are clearly their spare clothes on the side of the bed before straightening and folding his arms behind his back."

    s_beanie smile "Oh yeah, by the way, I'm Stan and this nerd is my brother Ford. Welcome aboard the Stan-O-War 3! What's yer name and where're ya from, anyway?"

    window hide

    python:
        _name = renpy.input(_("What's yer name?"), length=24).strip()
        player_name = _name or "Pat"

        _home = renpy.input(_("Where're ya from?"), length=40).strip()
        player_home = _home or "nowhere in particular"

        _pro = renpy.input(_("What're yer pronouns? (for example: she/her, he/him, they/them)"), default="they/them", length=24)
        set_pronouns(_pro)

    s "Pleasure to meet ya, [player_name]. So, how'd you end up in the middle of the Atlantic?"

    menu:

        "You were testing out a prototype watercraft.":
            p "Well, I was testing out a prototype submersible watercraft when the craft's Artificial Intelligence decided it wanted to explore the ocean on its own."
            p "It went rogue, ejecting me from the cockpit before diving out of sight."
            show ford finger at right, hop
            f "Ha! I would expect as much! I've never met an artificial intelligence that had an ounce of loyalty."
            f grin "Still, I'd love to hear more! That is fascinating work! I'm glad we happened along before you succumbed to the elements."
            $ approve("ford", 2)

        "You tumbled off a cruise ship while drunk.":
            p "Well, last I remember, I was in a drinking contest with a circus contortionist on a cruise ship."
            s smile "Sweet Moses! You fell off a cruiseliner? Those things are huge! That drop had to be a doozy. I hope you won, at least!"
            p "Yeah, me too."
            $ approve("stan", 2)

        "You were fishing alone.":
            p "I was fishing and stargazing when there was a strange noise and the sky went all red. That's the last thing I remember before waking up in the middle of the ocean."
            show ford grin at right, hop
            f "Fascinating! I wonder if you encountered a temporary wormhole, or if perhaps you were abducted by aliens! You'll have to tell me everything!"
            f smile "Once you're quite recovered, naturally."
            s smile "No way, poindexter! Once our new guest recovers, we're doin' some DEEP SEA fishin'!"
            s grin "I even brought the Joke Book!"
            f eyesclosed "{i}*groans*{/i}"
            $ approve("stan", 2)
            $ approve("ford", 2)

    show stan neutral
    show ford neutral

    "It occurs to you that you've only got the clothes on your back at the moment, and lacking any form of identity, air travel is out of the question."
    "Even if you did have enough in your bank account to pay for a trip home, you have nobody to call who'd be able to access it."

    p_think "What am I going to do now?" (show_act=_("thinking to yourself"))

    "Your head spins and you flop back down on the bunk with a weak groan. Beanie Guy reaches a hand out and feels the temperature of your forehead."
    "Out of the corner of your eye you see him exchange some subtle body language with his twin, who speaks up."

    f neutral "You should get some more rest. We'll wake you in a few hours for dinner, and then we can discuss our next move."

    "You'd thank them again if you had the energy, but you're already drifting toward unconsciousness."

    scene black with blackout
    pause 0.8

    scene bg bunk at wake

    "You wake up a few hours later, ravenous. You struggle weakly into the clothing that's been left for you and then call out."

    p "Guys? Hellooo?"

    scene bg galley at rocking
    show ford smile at right
    with dissolve

    "Ford responds to your calls, a warm smile softening his angular face when he sees you out of bed and dressed. He puts an arm around you and assists you to a small booth table in the cosy kitchen nearby."

    show stan neutral at enter_left

    "Stan saunters over and drops a plate of hot food in front of you. You tear into it like a wolverine, barely able to register the conversation they're having over your lowered head."

    ## [Illustration of a table full of hot dogs, rehydrated mashed potatoes,
    ## Pitt Cola, and cans of brown meat]
    scene cg dinner at slow_push with dissolve
    pause 1.2

    "Eventually, your shoveling slows and you slump into the corner of the booth. Ford insists that you drink more water, and once you've done so, Stan lifts your glutted body with a solid arm under your shoulders, ushering you back to what you now realize must be his own bunk."
    "You've gathered that the twins have been taking turns sleeping in Ford's bunk. You smile up at Stan from under the blankets, meaning to thank him, but you drift off too quickly."

    scene black with blackout
    pause 0.6

    with vpunch
    "Awakened by a sudden jarring of the boat, you hear directions shouted from the deck down to what must be a dock as the Stan-O-War 3 maneuvers carefully into a berth."

    scene bg bunk with dissolve

    "You feel the long, drawn out slide as the boat comes to rest against the dock. Moments later, Stan knocks lightly on the door of the cabin before entering."

    show stan smile at left with quick

    s smile "Welcome to Reykjavik! That's Iceland's main port, if ya didn't know."

    "Stan adopts a conspiratorial expression and leans closer to you."

    s neutral "Look, I know ya don't have the paperwork to get on a plane from here, but if you wanna try to bluff your way through, I can probably find somebody that can help..."

    "The exterior illumination is eclipsed as Ford's tall frame fills the doorway."

    show ford frown at enter_right

    f "No, Stanley! [player_name] is a resident of [player_home], and we will see [p_obj] returned home WITHOUT putting [p_obj] in danger of incarceration."

    menu:

        "Side with Stan.":
            p "I {i}could{/i} work with that. Unfortunately I don't have any money. I'm pretty sure forgers want cash, and the airlines usually want paying as well." (show_act=_("you turn to Stan"))
            show ford frown
            "Ford gives Stan a look."
            s neutral "Ok kid. We won't leave you hangin', no matter what. We'll find a way to get you home."
            p "Really?"
            s smile "You bet, kid."
            $ approve("stan", 1)

        "Side with Ford.":
            p "Could you actually do that? If you could get me home, that would be amazing!" (show_act=_("you turn to Ford"))
            f neutral "Indubitably. We're on a planet-wide search for anomalous activity. I'm sure there must be something to research that brings us near to your home."
            $ approve("ford", 1)
            p "Phew, you don't know how relieved I am to hear you say that."
            f smile "We're happy to help, right Stanley?"
            s smile "You bet, kid."

        "A weird, third option.":
            p "What if I just... Y'know, hang out with you guys until you end up somewhere I like? Hopefully somewhere with palm trees and frosty beverages? I can be helpful! Ehh?"
            s frown "I don't know... Are you sure that's what you want, kid? It can get pretty dangerous out on the ocean. Airline Security is nothin' compared to the things we've seen."
            s "Plus, the weather could stall us somewhere for weeks. You're signing up for a lot of salty clothes, crappy food, endless ocean, and Sixer monologuing about nerd stuff. All. The. Time."
            show ford frown
            "Ford looks at you meaningfully after a sidelong glance at Stan."
            f "This is not a comfortable life, [player_name]. We spend a lot of time in peril, or simply enduring monotony."
            f neutral "Then again, I'd really like the chance to run some tests on you and research your predicament on the off chance that the cause was anomalous."
            p "I, uhh... sure, ok. Yeah, that sounds fine I guess."
            s neutral "What do you think, Sixer? It'd be nice to have someone else to talk to for a while." (show_act=_("gives Ford a sidelong glance"))
            f neutral "As long as they're aware of the dangers, I'm for it." (show_act=_("gives Stan a sidelong glance"))
            show stan grin at left, hop
            show ford grin at right, hop
            with quick
            with vpunch
            twins "You're in, [player_name]!!" (show_act=_("in unison, yelling"))

    jump arrive_at_reykjavik


################################################################################
## Arrive at Reykjavik
################################################################################

label arrive_at_reykjavik:

    scene black with dissolve
    call chapter(_("Arrive at Reykjavik"), _("Iceland's main port"))

    scene bg street with slowfade

    "The three of you wander through downtown Reykjavik, stocking up on supplies and gear. The guys generously purchase you an anorak and sundry other cold weather necessities, extra clothes and underthings, and a bathing suit."
    "They also purchase a hammock to hang from the Stan-O-War 3's beams to act as a makeshift bed."

    scene bg dock
    show stan neutral at left
    show ford neutral at right
    with dissolve

    "After delivering these things to the boat, you all stand on the dock and debate what to do with the rest of the afternoon."

    f smile "I'd love to visit the Whale Museum! I have long suspected that a narwhal horn specimen housed there is mislabeled."
    f grin "It's possible that the horn isn't that of a narwhal and may actually be evidence of an entirely unknown species!"

    s frown "{i}*groan*{/i} Haven't we seen enough fish to last us a lifetime?"

    f frown "Whales aren't fish, Stanley."

    s frown "Dammit Sixer, that's not the point!"

    s neutral "Y'know, Mabel said something about music clubs with hot tubs around here, we should look for one o' those!"

    f neutral "There is also a local film festival scheduled for tonight. A documentary filmmaker I'm familiar with through her work on the topic of Icelandic cryptids is showcasing a new film."
    f "Regrettably, I believe it to be a departure from her previous work; tonight's film seems to be a period drama set in turn of the century Iceland."

    s embarrassed "That... uhh... doesn't sound {i}terrible{/i}."

    s neutral "Tell ya what, if that's what the kid wants to do, we'll all go. If not, how 'bout we split up and [player_name] can tag along with whoever [p_subj] [p_wants]?"

    f neutral "That sounds reasonable."

    s smile "Whaddaya say, [player_name]?"

    menu:

        "Join Stan for soaking and sipping on the town.":
            p "Hot tubs, booze and tunes? You're singing my song, Stan! Let's do this!"
            show stan smile at left, hop
            s smile "Yeah! Let's go get our swimsuits on and fancy ourselves up. We're paintin' the town whatever color you want tonight!"
            f neutral "Just be careful, Stanley, and message me if anything happens. I'll meet you two back here later tonight."
            s smile "Sure thing, Ma. Have fun with the fish!"
            f frown "Whales are not fish!"
            $ approve("stan", 1)
            jump stan_after_dark

        "Join Ford for an educating journey and a mystery to solve.":
            p "I love museums! Speaking of museums, the Phallic Museum is right down the street! I wonder if it's open."
            p "We should go there afterward; I bet they have an anomalous wang on display, we just have to find it!"
            f uncomfortable "Um, yes... indeed. I'll just grab my bag and we'll be off."
            s smile "Uh oh, he's bringin' his Science Bag. You're in for it now."
            p "Is that bad?"
            s grin "I'm outta here! Meet you guys back here tonight ok bye!"
            hide stan with moveoutleft
            $ approve("ford", 1)
            jump a_night_at_the_museum

        "Take them both to the Theater.":
            p "I don't think we should split the party. Who knows what evils lurk in the cold streets of Reykjavik? Let's go watch the movie and critique it later according to our own criteria!"
            s grin "We can even make it a drinking game if we go get a fifth of whiskey."
            p "Yeah! Every time someone broods on a windy clifftop, that's a sip."
            s grin "Every time the servants defy the leader of the household and help one of the noble daughters who's fallen in love with someone they don't deem appropriate steal away to be with her lover, that's a sip!"
            p "Wow, you've really given this some thought."
            show ford shocked at right, hop
            f shocked "Wait, did you just make a DD&MD reference, [player_name]?"
            p "Mmmaybe... Anyway, we've got a destination, let's GOOOOOO!"
            $ approve("ford", 1)
            $ approve("stan", 1)
            jump reykjavik_international_film_festival


################################################################################
## A Night at the Museum
################################################################################

label a_night_at_the_museum:

    scene black with dissolve
    call chapter(_("A Night at the Museum"), _("Ford and the False Narwhal"))

    scene bg street dusk
    show ford neutral at center
    with slowfade

    "You're delighted to discover that Iceland's Whale Museum is only a couple of blocks away from the dock."
    "As the two of you make the short trek, Ford expounds excitedly regarding the difference between the common Narwhal and the remains that are on display."
    "The cryptid, which Ford has dubbed the \"False Narwhal\", has only been seen a few times. Not much is known about it."
    "He believes the animal was caught by untrained hands many years ago, and the horn was mistaken for the horn of the much more common whale."

    p "Huh, bummer. I was hoping for something more mysterious and paranormal."

    f smile "Unfortunately, science is often quite banal. However, without the boring parts of science, the inexplicable phenomena wouldn't hold as much import, wouldn't you agree?"

    menu:

        "You're dubious.":
            p "Uhh, sure. Whatever you say?"
            show ford uncomfortable
            "Looking a bit deflated, Ford smiles and nods, striding ahead with purpose."
            $ approve("ford", -2)

        "You agree.":
            p "Oh, absolutely! Without the rigors of the scientific process, how can we tell the difference between the {i}natural{/i} and the truly {i}supernatural{/i}?"
            "Ford's eyes light up."
            show ford grin at center, hop
            f grin "Exactly! We can't even begin to speculate on the unknown until we've made absolutely sure that it {i}is{/i} unknown using the technology currently at our disposal."
            $ approve("ford", 2)

        "You disagree.":
            p "What?? The scientific community is {i}full{/i} of frauds and number-fudgers! Don't they ostracize anybody who wants to research anything deemed 'paranormal'? Why bother with mainstream science? It's all baloney!"
            f smile "Yes, well. It'd be nice to work in a vacuum, not having to rely on the oversight of others, but science wouldn't get anywhere without the convergence of many minds producing copious amounts of data."
            f neutral "Even if some of it has been falsified, that which isn't is invaluable to science's ultimate goal."
            $ approve("ford", 1)

    scene bg museum
    show ford neutral at center
    with slowfade

    "Inside the museum, you are greeted by life sized whale sculptures, perfect down to the barnacles and lice that generally adorn the behemoth's tough, rubbery skin."
    "Ford is a volcano of information that continues to erupt as you wander through the exhibits. You consider telling him that you know most of this already, but he seems so delighted to impart this knowledge that you can't bring yourself to stop him. His enthusiasm is contagious."

    scene bg horn
    show ford grin at center
    with dissolve

    f grin "Aha, here we are!"

    "While most of the exhibits are sculpture replicas, the \"Narwhal Horn\" is solidly actual, sitting behind a velvet rope."
    "It's an impressive three meters long and looks, to you, like the horn of a unicorn that undoubtedly suffered from chronic neck pain. Ford is studying its root closely with a triumphant expression."

    show ford finger at center, hop
    f finger "Yes, just as I suspected! This horn is not ivory at all, and moreover, it's a {i}right-handed{/i} helical spiral, meaning it isn't a Narwhal horn!"

    menu:

        "What the heck are you talking about? It looks like a Narwhal horn to me.":
            f frown "But, you see, the helical form is... never mind."
            $ approve("ford", -1)

        "Whoa, no way! It's helically reversed! We need to take a sample of this, like now.":
            f grin "I'm ready when you are."
            p "I'm so ready, tell me what to do!"
            $ approve("ford", 2)

        "How are we going to take samples if we can't touch it? Did you contact the museum? I'm sure they'd let you run some tests.":
            f frown "I did, but the answer is tied up in so much red tape that I've decided to take matters into my own hands."
            p "Ok then, what's the plan?"

    f neutral "I'm going to head to the bathroom on the left. I will wait there while you use this item by rubbing it against the artifact repeatedly until a viable sample is collected."

    p "Is this a bunion shaver?"

    f blush "It was the most effective item I could find for this purpose. Are you in or not??"

    p "Of course! I'll head into the bathroom when I'm done."

    hide ford with dissolve

    "The long spiral horn is held in an alcove behind an informative plaque about the majestic Narwhal."
    "You do your best to be inconspicuous as you lean over the large plaque and stretch your arm out to scrape the horn with the implement that Ford provided. It's not easy. Only a sprinkling of material comes off."
    "You persist as long as you think is prudent before sweeping the tiny pile of shaved horn into your gloved hand and making a break for the bathroom."

    scene bg bathroom
    show ford grin at center
    with dissolve

    f grin "Brilliant, come in, come in!"

    "You duck into the bathroom to find that Ford has set his 'Science Bag' on the counter and spread several unidentifiable mechanisms around it. He holds out a petri dish and you dump the horn shavings into it."

    p "Why couldn't you have run these tests on the boat?"

    f neutral "I'll need to observe the oxidation of the newly-exposed particles as soon as possible. This should only take a few minutes. You can feel free to enjoy the museum while I run the tests, if you like."

    menu:

        "Sure thing, I'll wander back here in a few minutes.":
            scene bg museum with dissolve
            "Ford nods distractedly as you turn and exit the bathroom. You meander around the museum, learning more about whales than you ever wanted to know."
            scene bg horn with dissolve
            "Having exhausted your attention span, you wander back toward the Narwhal horn exhibit and the nearby bathroom. You notice a couple of people hunched over the horn itself, speaking animatedly. One of them is in a uniform."
            "You shimmy over to the bathroom door and crack it open."
            scene bg bathroom
            show ford neutral at center
            with dissolve
            p "We've been made, Ford. Time to boogie!" (show_act=_("whispering"))
            f frown "Excuse me?"
            p "They called Security! We gotta go!"
            show ford shocked
            "Ford stows all of his instruments into his bag without hesitation and you're spun around as he hooks his arm with yours and exits the bathroom at speed. He marches you quickly to the exit as shouts ring out behind you."
            with vpunch
            f shocked "{b}RUN!{/b}"

        "Should I stand watch?":
            p "What if someone notices what we did!"
            f frown "Well then, we shall deal with that when and if it occurs."
            show ford neutral
            "You stand nervously near the door as Ford tests the particles of horn in several unidentifiable mechanisms."
            show ford frown
            "Harrumphing to himself, frowning..."
            show ford grin
            "...and grinning at different intervals..."
            show ford finger at center, hop
            "...and finally shouting \"AHA!\", Ford completes his tests."
            "You hear raised voices from the museum and peek out of the bathroom to see a couple of uniforms and an attendant clustered around the horn exhibit."
            p "Ford, we gotta go. We're busted."
            show ford shocked
            "Ford stows all of his instruments into his bag without hesitation and you're spun around as he hooks his arm with yours and exits the bathroom at speed. He marches you quickly to the exit as shouts ring out behind you."
            with vpunch
            f shocked "{b}RUN!{/b}"

        "I'm curious to see what you're testing the sample for, if that's ok.":
            f smile "Certainly! Here, add the contents of this vial to the sample while I calibrate the instruments."
            "Ford fiddles with the various apparati as you pour a small vial of clear liquid into the petri dish."
            "Finally, he pulls on some six fingered rubber gloves before reclaiming the sample."
            p_think "Wait, SIX FINGERS? Whaaaat?"
            "As he feeds it to the various devices, he dictates his actions to you in a low, even voice. You are fascinated."
            "Some of it is beyond your grasp, but most of it is familiar enough for you to understand that this sample didn't come from a Narwhal, but instead from an animal with properties that are not wholly understood by current science."
            "You are only pulled out of your nearly trance-like attention by the sound of raised voices in the hallway."
            p "Oh no, I think we're in trouble. Ford, we gotta go!"
            show ford shocked
            "Ford stows all of his instruments into his bag without hesitation and you're spun around as he hooks his arm with yours and exits the bathroom at speed. He marches you quickly to the exit as shouts ring out behind you."
            with vpunch
            f shocked "{b}RUN!{/b}"
            $ approve("ford", 2)

    scene bg street night at running with dissolve

    "The moment you exit the museum, Ford has clamped his arm around yours and is sprinting back the way you came."
    "He's doing the lion's share of the running and your feet barely touch the ground as you hear shouts ring out behind you."
    "A corner is turned, and then another, and finally Ford slows enough for you to find your footing and speed-walk alongside him toward the dock and the Stan-O-War III."

    scene bg pier night
    show ford grin at right
    with dissolve

    f grin "Well done! I've still got some further tests to run, but tonight was a total success!"

    p_think "How does he not seem winded at all?"
    p "Sweet! I'm happy to help. I wonder how late Stan will be out."

    f neutral "We can expect him anywhere between now and never. If dawn comes and he's not back, we'll go get him." (show_act=_("sighing"))

    p "Shouldn't we go now? What if he's too drunk to find his way home or something?"

    "As you finish speaking, you hear a scrabble of footfalls on the icy pier and recognize Stan's silhouette as he reaches the Stan-O-War III."

    show stan anxious at enter_left

    f smile "Ask and ye shall receive, eh?"

    p "There you are, Stan!"

    s anxious "Anybody followin' me down the pier?"

    f neutral "Not that I can see. I think you've pulled it off, whatever 'it' was."

    s grimace "Great, now where's my orthopedic back pillow?"

    jump outro


################################################################################
## Stan After Dark
################################################################################

label stan_after_dark:

    scene black with dissolve
    call chapter(_("Stan After Dark"), _("Soaking and sipping on the town"))

    scene bg pier night with slowfade
    show stan grin at center with dissolve

    "Stan dances out of the Stan-O-War 3 in a white suit with a burgundy dress shirt, its top buttons open and displaying an almost worrying amount of chest hair."
    "He wraps his anorak around him before exchanging some cautionary words with Ford as they part ways."
    "Dressed as best you can in your own clothes, wearing your bathing suit underneath, you once again thank your lucky stars that of all the mariners that could've scooped you out of the ocean, it was these two generous, likeable dudes."

    p "Aaah, crap. It just occurred to me; they're going to want ID at the door, aren't they?"

    s neutral "Don't worry about a thing, kid. Once we're there, follow my lead. No questions."

    p "Uhhh... okay."

    scene bg club street
    with slowfade

    "Throbbing bass can be heard even before you round the corner of the street leading to the club. You're pretty sure you can feel it in the soles of your new boots."
    "A brightly colored sign declares 'Monkey Bar', lighting up the surrounding street with dazzling neon rainbows."

    "You're surprised when Stan sticks to the shadows on the far side of the street and bypasses the club, ducking down a dark alley beside it, with you on his heels."

    "Stan sniffs the air and stops at a chained opening in a tall fence. He peers through a crack for a moment before pulling something out of his pocket."
    "You see a flash of metal in his hand as he manipulates the padlock, which opens easily. Next thing you know, he's pulling you through the fence and closing it behind you."

    scene bg club alley
    show stan neutral at left
    with dissolve

    "You find yourself in a shadowy nook behind the club. It boasts a couple of garbage bins, and a sand-filled bucket sits by a propped open fire door."
    "Stan pats his pockets and brings out a cigar case, popping it open to reveal a half-smoked stogie that he pops into his mouth."
    "You're still marveling at the speed with which he popped that padlock when the door to the club opens and a man in nothing but a speedo comes out holding a cigarette and lighter. Stan turns to him."

    show patron at farright with dissolve

    s "Oy, áttu kveikjara takk?"

    patron "Ekkert mál."

    "The man graciously steps up to light Stan's cigar, cupping the flame with his other hand. You notice a smeared stamp on the back of his hand that looks like a cartoon monkey face."

    "Puffing on his cigar, Stan steps back and thanks the man with a \"þökk fyrir\". The two of you move to huddle on the other side of the enclosure."
    "Stan pats his pockets again and pulls out a handful of disparate writing utensils. He selects one and stows the rest."

    p "What the {i}heck{/i} are we doing?"

    s frown "Sshh."

    "Stan flicks his eyes toward the smoker. Once the man finishes his cigarette and reenters the bar, Stan relaxes."

    hide patron with dissolve

    s neutral "Gimme your hand."

    "You reach out and he grabs your hand, uncapping the writing utensil, a blue ballpoint pen, with his mouth. He begins to draw on your hand, occasionally using his thumb to smudge the lines."
    "When he releases it, you take a look at his work. It looks identical to the blue monkey stamp you saw on the hand of the other patron. He gets busy drawing on his own hand."

    menu:

        "\"Stanley, you are the coolest person I have ever met.\"":
            p "Stanley, you are the coolest person I have ever met."
            s blush "Heh, I have my moments. You did great too, kiddo!"
            p "But I didn't do anything!"
            s grin "Exactly! You didn't balk, you didn't sweat, you didn't backpedal. You're a natural. Now to get some free drinks."
            $ approve("stan", 2)

        "\"Are you sure this is a good idea? What if they don't buy it?\"":
            p "Are you sure this is a good idea? What if they don't buy it?"
            s neutral "Trust me, kiddo. This is kids' stuff. You should try breaking out of a government facility while floating around in zero gravity."
            p "What?"
            s grin "Don't worry about it. Now to get some free drinks."

        "\"Wow. No wonder you've been to jail multiple times.\"":
            p "Wow. No wonder you've been to jail multiple times."
            s frown "Hey, everything's legal if there're no cops around."
            $ approve("stan", -1)

    scene bg club
    show stan neutral at left
    with slowfade

    "Stan leads the way into the club. Nobody stops you as you weave between naked, sweaty bodies toward a wall of cubbies."
    "Stan shucks his clothes down to a pair of tropical patterned swim trunks. You follow suit, stowing your clothes in the cubby with Stan's before following him into the center of the club."
    "Stan takes a look at one of the crowded hot tubs and winces."

    s grimace "Ehh, on second thought, sitting in what's essentially old man soup doesn't have the same appeal in reality that it had in my head. Wanna try the sauna room instead?"

    p "Yeah, that water is probably full of arthritis ointment. I'm with you."

    scene bg sauna
    with slowfade

    "You find a spot on one of the wooden benches in the crushing, oppressive heat, sweat beginning to roll down your body. It's actually quite nice compared to the raw chill outside."
    "Stan disappears for a few moments and reappears with two cans of beer which immediately bead up with condensation."

    show stan smile at center with dissolve

    s smile "Here ya go, kiddo. I hope ya like weird foreign beer."

    p "Any port in a storm!"

    show stan laugh
    "Stan cackles as the two of you crack open your beers, and Stan gestures for a toast."

    s smile "Let the party begin! Whadda we toast to?"

    menu:

        "\"To Stan Pines, hardened criminal and magnificent seaman!\"":
            p "To Stan Pines, hardened criminal and magnificent seaman!"
            show stan laugh at center, hop
            s laugh "Hahah! You're a riot, kid."
            $ approve("stan", 2)

        "\"To the Stan-O-War 3 and its heroic captains! Without you guys, I'd be fish food.\"":
            p "To the Stan-O-War 3 and its heroic captains! Without you guys, I'd be fish food."
            s grin "Yeah, to the Stan-O-War 3! It took a lifetime to get her, but it was worth the struggle."
            show stan blush
            p_think "Are his eyes a bit dewy right now or is it the heat in here?"
            $ approve("stan", 1)

        "\"To free drinks, sloppy security and public nudity!\"":
            p "To free drinks, sloppy security and public nudity!"
            s grin "You said it, [player_name]!"

    show stan neutral

    "Many of the patrons are nude. They tote around small towels to place on the benches before they sit and chat away just as they would in a cafe."
    "While the clientele are varied, the vast majority of them are men, on the older side. It's becoming difficult to find a place to aim your eyes, so you focus on Stan."
    "At first you're grateful that Stan seems content to remain in his swim trunks, but the more you consider the idea, the more you find your eyes roaming over his solid, sweating and obscenely hairy body."

    "Your eyes travel back up to Stan's and find them scanning the room. But... did you see him dart his eyes away from you just a second after you looked?"

    show stan embarrassed
    "He upends his beer and shakes the last drop into his mouth. You do the same, and he swipes your empty can and disappears for less than a minute before coming back with two cold ones."

    s neutral "So... [player_name]. If you're gonna bunk with us for a while, you should know some things. Sixer... uh, Ford and I have been through some stuff. We both have a bit of a hair trigger."
    s "What I mean is... probably you shouldn't sneak up on us or like, wake us up by shaking us or something. We tend to, uh... lash out."
    s "You don't have to walk on eggshells or nothin', just try not to spook us, ok?"

    p "Yeah, I understand. Thanks for warning me." (show_act=_("you nod, a little concerned and a lot curious"))

    "The two of you sip your beers and sweep your gaze over a panorama of wrinkly genitals for a few more minutes before Stan speaks again."

    s frown "Whoever the DJ is should be drawn and quartered, or possibly tarred and feathered. One of those old-timey deaths, to match the intensity of what eardrums are goin' through right now."

    "As you're about to respond with a similar opinion, another wrinkly ballsack turns to face you and Stan. You look up to see a scrawny chest and above that, a helmet shaped like a lizard head. A muffled voice emerges from within."

    show stan neutral at left with move
    show lizard at farright with dissolve

    lizard "Hvað sagðirðu?"

    s anxious "Oh eh, heheh, we were just joking around. Bara grín!"

    lizard "Your accent is atrocious, and who the hell are you? This is the album release party! We're supposed to have this place to ourselves. I'm calling security."

    hide lizard with moveoutright

    "Before Lizard Head had even gotten three strides away, Stan grasped your wrist and dragged you through the throng toward the cubbyholes."

    scene bg club at running
    show stan anxious at center
    with dissolve

    s anxious "Get dressed faster!"

    p "I'm trying! Pulling on pants is so hard when you're wet!"

    scene bg club street with dissolve

    "There are raised voices back in the center of the club as you pull on your boots. Stan practically drags you out the front door."
    "There are a couple of taxis parked outside, and he leans into one of their windows. You can't catch what was said inside, but as Stan ushers you to a nearby alley and pulls you into the shadows, you hear the taxi burn rubber, leaving the area at high speed just as the club doors open."
    "Lizard Head is there with a few others. All are speaking Icelandic rapidly, but you sense defeat in their tones as the taxi speeds out of sight. Stan lets out a relieved sigh."

    scene bg club alley
    show stan embarrassed at center
    with dissolve

    s embarrassed "Well, I guess that's enough fun for one night. Sorry about all the law breaking and the running and the... everything else..."

    menu:

        "Are you serious? This has been one of the best nights of my life!":
            p "Are you serious? This has been one of the best nights of my life! Stan, I know I'm standing here shivering because my wet bathing suit is soaking into my clothes, but I wouldn't change a moment of it!"
            show stan grin at center, hop
            s grin "I knew you were a kindred spirit, ya little hellion! Now, let's get back to the boat and get into some dry clothes. I'm freezing my balls off!"
            $ approve("stan", 2)

        "This is HEAVY, Stan! What if I get taken to ICE JAIL?":
            p "This is HEAVY, Stan! What if I get taken to ICE JAIL! I don't want to get turned into a snowman!"
            s grimace "Relax, kid, they're off our trail now. We just need to get back to the Stan-O-War 3 without freezing our asses off."
            p "Yes please. Put me back in the boat!"
            $ approve("stan", -1)

        "Good, they're distracted. We've got to get back to the boat.":
            p "Good, they're distracted. We've got to get back to the boat. It's down that road, right?"
            s neutral "Sure is. Follow my lead."
            $ approve("stan", 1)

    scene bg cabin night
    show stan smile at left
    with slowfade

    s smile "Whoof! Home Sweet Boat!"

    p "You said it. I feel like a drunk raisin. Wait a minute, shouldn't we wait up for Ford?"

    show ford grin at enter_right

    f smile "That won't be necessary. I was able to retrieve a sample and run some tests, and you won't believe what I've discovered!" (show_act=_("stepping in from his lab"))

    s smile "Save it for tomorrow, nerd. The kid and I are tuckered out."

    p "Quit it with the 'kid', Stan, I am an adult!"

    jump outro


################################################################################
## Reykjavik International Film Festival
################################################################################

label reykjavik_international_film_festival:

    scene black with dissolve
    call chapter(_("Reykjavik International Film Festival"), _("Dinner and a drinking game"))

    scene bg street night with slowfade

    "After an extended period of waiting for Stan to be satisfied with his ensemble for the night, the three of you finally disembark toward the theater."
    "Looking at his Omniwatch, Ford steers you past the theater, leading you on what turns out to be a much longer route to a liquor store."
    "On the way you pass by the world's only Phallological Museum, and you make a few humorous remarks that have Stan guffawing and Ford blushing madly."

    scene bg theater with slowfade

    "A sea of anoraks mill around you and Ford as you shuffle toward a row with three free seats. You push Ford in first, not wanting to be caught on the edge of the banter."
    "The lights dim, and finally you hear Stan grumbling his way past knees to get to you, laden with a cornucopia of snacks and popcorn."

    show bg theater at slow_push

    "From one side comes a tide of pedantry regarding the movie's anachronistic props and scenery. From the other, a volley of grumbles and shouts aimed at the characters on the screen."
    "You munch on popcorn and sweets. Eventually a bottle is passed around and the twins begin marking out shot-triggering tropes and sip-worthy scenes."

    with vpunch
    "Finally, with a roar of indignance from Stan, the final act plays. There is a smattering of applause from the room until a thank-you to the director is announced over the intercom, disclosing her attendance."

    "The audience swells with more applause, but not before Ford and Stan spring out of their seats intent on speaking to the woman herself. You grab their sleeves to prevent yourself from being lost in the crowd."

    scene bg theater
    show stan frown at left
    show ford frown at right
    with dissolve

    f frown "Did you see the markings on the rocks in the first scene with the protagonist? The same symbols appear, all nearly obscured by darkness, throughout the piece. It must be a cipher, but I can't crack it without more information!"

    s frown "There is NO WAY it's supposed to end like that. They musta had some kind of issue that made it impossible to shoot the right ending. Maybe the actors got sick or somethin'. I need to know!"

    "You cling desperately to the guys as they barge their way to the front of the mob. The crowd seems tame until Stan and Ford barrel through on their mission."

    show stan grimace
    show ford shocked
    with vpunch

    "Someone takes umbrage with the twins' rough urgency and has words with Stan. Before you know it, a brawl has broken out."

    with hpunch
    hide stan
    hide ford
    with dissolve

    "You duck behind a row of seats and wait until you can see both Stan and Ford."

    show stan anxious at left
    show ford frown at right
    with quick

    "Leaping over the seats, you grab both Stan and Ford by the collars and make it clear that the time to exit is nigh. They seem to come out of their violent reverie and both nod."

    scene bg street night at running with dissolve

    "Ducking through the now agitated mass of puffy arctic clothing, you all find your way to the exit just in time to hear sirens."
    "With a wild look shared between you, the three of you bolt down the street in the shadows, ducking through alleys and skidding around icy corners until you finally make it back to the Stan-O-War III."

    jump outro


################################################################################
## Outro
################################################################################

label outro:

    scene black with dissolve
    call chapter(_("Outro"), _("Home Sweet Boat"))

    scene bg storage at rocking with slowfade

    "The three of you toss quick stories back and forth as you prepare for bed. Stan clears space in the storage room while Ford helps you hang your hammock from the rafters, taking some time to also enlighten you on the correct way to use a hammock."

    "After wrapping yourself in your blankets and lying crosswise in the hammock, you descend into slumber with a smile."

    window hide
    pause 1.0
    call screen the_end with slowfade

    return
