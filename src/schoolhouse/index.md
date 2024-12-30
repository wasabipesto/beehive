# Renovating The Old Schoolhouse

What is air conditioning? What is air, actually? What makes it comfortable or uncomfortable? Healthy or unhealthy? How do you measure it? How do you manipulate it? And how do you do so while spending as little energy as possible?

## Air is weird

Air is great. Everybody loves air. You’ve got Oxygen, the star of the show. Carbon dioxide, plants love that stuff. Nitrogen, which is presumably important for something. Add a dash of Argon a pinch of “other” and you’ve made the pie chart from every 3rd grade science book. But that’s not what we’re here to talk about, really.

1. The air is wet! There’s usually more water in the air than Argon! I could rant about this for an hour, but humidity changes everything. Too much or not enough humidity can be a health issue, but way before that you’ll notice if the air is too dry or sticky. Water in the air takes a lot of energy to condition or remove, so it’s usually one of our first priorities.
2. Even a tiny amount of bad stuff is bad. Smoke and exhaust can contain aerosolized heavy metals and carcinogens that are dangerous and hard to measure. Your body can catch most of the larger particles, so the smaller ones are typically more concerning. Instead of trying to measure individual particles, we take samples and measure the number of small particles under a certain threshold (2.5 or 10 micrometers across, known as PM2.5 or PM10 respectively).

## So what are we trying to do here

Let’s look at all of the things about the air we’re going to try to control:

- Temperature: People are most comfortable around 70F and can notice very slight changes in temperature. They also like to be able to request a higher or lower temperature.
- Humidity: Dependent on temperature, most people okay anywhere from 20 to 80% relative humidity. Comfortable levels are generally between 30 to 50%.
- Carbon dioxide: CO2 builds up in a space over time as people exhale, and can make them feel drowsy or distracted. Higher concentrations can make the room feel stuffy.
- Particulates/Odor: Not all small particles are harmful, but they can be annoying and we should try and keep them out of the air anyways.
- Energy/Cost: We should do all of this while using as little energy as possible - which also means reduced costs.
- Maintenance: Whatever is installed should be easy and cheap to maintain and repair.
- Freeze Protection: If your application is in a location that can drop below 32F, your solution needs to be resilient against freezing.

That’s a lot when you say it out loud, but some of these problems can be solved with the same strategies. Let’s look at a few examples.

# The Old Schoolhouse

Around the midwest (where I live) you’ll see a lot of old schoolhouses. Historic monuments, beautiful brick exteriors, and no air conditioning. Let’s say you’ve been asked to sprinkle some HVAC in there to keep nine-year-olds comfortable while they learn about the different types of cloud.

## Solution #1: PTAC

If you’ve stayed at a hotel you’ve probably seen a packaged terminal air conditioner, or PTAC for short. These little guys sit underneath the window and provide a nice stream of cool or warm air, as requested by the little dial on the side or a remote thermostat out in the room. They’re fairly cheap and easy to install so let’s drop one of these in every classroom and see how they do.

### Temperature ✅

Assuming the units are properly sized, they actually do a pretty good job at keeping the space at the target temperature.

For cooling we have a small refrigeration circuit, much like a small air conditioner you’d fit in a window. The circuit exposes cold fluid to the interior, cooling down the air, while radiating that heat outside. This also takes a fair bit of energy, plus a charge of refrigerant to actually run the system.

For heating, we picked a unit with resistive heating. This works like a hair dryer or space heater, pushing electricity through an element to heat it up. Unfortunately it takes a lot of energy: we had to install a new circuit for each classroom in order to get enough electrons. The school needed a new electrical switchgear anyways.

If we wanted, we could add a heat pump to the heating side. It utilizes the same refrigerant as the cooling side, so it doesn’t add much complexity to the system. The system would still utilize the resistive element for quick warm-up and for extremely low temperatures, but during typical use the heat pump would effectively run the refrigerant “backwards”, cooling the outside air and heating the inside. The benefit here is lower energy costs when it’s between 30 and 50F outside.

An added plus here is that neither of these systems are vulnerable to freezing temperatures, so we can check that one off our list as well ✅

### Humidity 🚫

This unit can’t really control the humidity in the space. Why is that?

In order to dehumidify air we exploit one of its weird properties: warm air can hold more moisture than cool air. To remove moisture from air, we just cool it down until the air can’t hold the moisture anymore and then keep cooling it down even further. The moisture condenses into droplets, hopefully into a drain pan, and you’re left with cold, dry air. So as long as you can cool the air, you can dehumidify it somewhat.

The problem here is that in order to get enough moisture out of the air to bring it into our humidity comfort range, it’s much colder than we would find comfortable. As a rule of thumb, you’re generally cooling air down to around 55F in order to get the humidity low enough to be comfortable. This is too cold for… basically anyone. Typical dehumidification control requires you to be able to cool the air (all the way to 55F!) and then heat it back up (to 70F!).

Unfortunately our little PTAC units aren’t designed to be able to run both heating and cooling at the same time. They can cool down the air, which may remove some moisture if it’s really humid outside, but they can’t bring the indoor humidity down very far at all.

### Carbon Dioxide/Particulates/Odor ✅

Good news: it’s actually pretty easy to deal with carbon dioxide, particulate matter, and odor all at once. Fresh air! Get some nice outdoor air, bring it on inside, and let it push all of the bad stuff out.

There are a couple of things to keep in mind, however.

1. The fresh air needs to be conditioned. The more outside air you bring in, the more your cooling and heating systems need to work to make the space comfortable. If you’re dehumidifying at all, you’re going to need to do it a lot.
2. That fresh air is usually cleaner than the indoor air but it isn’t perfectly clean. You probably want your indoor air to have less than 1000ppm of CO2 and 20µg/m³ of PM2.5. Outdoor air is usually lower than that, around 400ppm of CO2 and 10µg/m³ of PM2.5, but can be as high as 900ppm of CO2 and 100µg/m³ of PM2.5 in dense or smoky environments.
3. In order to get all that particulate out you’ll need filters in the unit, and if you want to filter out more particulate you’ll need bigger filters. If you have bigger filters you’ll need a bigger fan. If you have a bigger fan, you’ll need more electricity.
4. You’ll need some extraction fans to help get that bad air out. Usually you can put these near the source of the particulates/smell, like in a bathroom or a kitchen fume hood. More fans means... more electricity.

### Energy/Cost/Maintenance ⚠️

There’s a reason you see these units everywhere: they’re cheap to buy and cheap to install. There’s very little specialty trade work involved, and most come prepackaged with just a single power connection.

The downside is that they suck power and they’re hard to maintain. The fans are actually a minority of the total power draw, most of the energy goes to the heating or cooling systems. Neither system is particularly “inefficient”, especially if you sprung for a heat pump, but they still take a lot of electricity.

Each room has its own individual fan motor, refrigerant charge, heating element, and filter bank, so regular maintenance requires inspecting every unit in every room. Repairs often involve disassembling the entire unit since it’s so tightly packed, and build quality is often shoddy. You need maintenance personnel who know how to work with refrigerant or a service contract with someone who does.

### Overall 🆗

If you’re the engineer for this job, these facts will cross your mind but you might still pick this option anyways. Old schoolhouses often have little space for mechanical piping or ductwork, and with a low number of rooms the maintenance burden will be lower. The overall cost of installation is still important, and while it may not be great at dehumidification the kids will be able to learn about the water cycle in nice, cool 70F rooms.

## Solution #2: Hydronic Unit Ventilators

What if, instead of lots of little heating and cooling elements, we had a big, central one of each? Our maintenance guy would certainly be happier, moving all of his repair work into one room. Our energy bill will be happier, since these bigger systems are more cost-efficient. Our upfront cost is a bit higher, but let’s see if the trade-off is worth it.

### Temperature ✅

Before, we had a small refrigeration circuit that directly cooled down air. This time, we’ll make one huge circuit and use it to cool down a pipe of water to about 40F. This is our big ol’ chiller, and it discharges that heat outside using the exact same refrigerant cycle. Then, we’ll run that pipe of cold water up to each individual unit in each classroom, and let it run through a thin coil that the air passes through, cooling it down.

We’ll do something similar with the heating side: instead of resistive heating elements, we’ll use gas-fired boilers. You can get electric ones, but here in the midwest gas is way cheaper and newer boilers have an incredibly high efficiency. These boilers will heat up water to around 140F and we’ll pump it out to heating coils set right after each cooling coil.

### Freeze Protection ✅

So now we can cool and heat the air however much we want. Water is excellent at holding and transferring heat, so we can size these coils as large as we want. Unfortunately, water can also freeze. We have a couple options to prevent this:

Add some antifreeze! The same stuff that goes in your car or your vape pen can help keep your coils from bursting. When you mix a little bit of ethylene glycol or propylene glycol into your hydronic supply water it will drop your freezing point by a few dozen degrees at the cost of slightly reduced heat capacity. You’ll especially want to do this if your chiller heat exchanger is outside.

Keep that water moving! If the water in your coil gets too cold it will freeze (and expand (and burst your coils (bad))) but if your water doesn’t stay in the coil long enough to get cold it won’t freeze. If you just have a couple big coils outside then this is usually a pretty good solution.

Don’t let the air touch it! What if there was a separate path that the air could take, completely bypassing the water coils, when it’s too cold? We can use a couple control dampers to redirect air around them in this situation, at the cost of making our units slightly larger. This used to be more common when hydronic flow control valves were, uh, optional.

### Humidity ✅

We can do this one now! We can size our hydronic coils as large as we want, and run them both at the same time! When it gets really humid out, inside the unit we’ll have the cooling coil fully open, chilling the air all the way down to around 55F before the heating coil warms it back up to where we want the room temperature to be. This move is super effective.

### Carbon Dioxide/Particulates/Odor ✅

We’re doing the same thing as before to address these items: bring in more outside air. We still have to worry about conditioning it, filtering it, so on and so forth, but there’s no getting around that.

### Energy/Cost/Maintenance ✅

Each of these units are a little more expensive to install, plus the cost of the hydronic piping, chillers, boilers, pumps, variable frequency drives, and controls to run it all, but once it’s installed the running costs are much lower. Maintenance at the unit is limited to replacing filters and occasionally repairing fan motors or blowing out coils. The rest of the maintenance is kept in the mechanical space (AKA the facilities office) where issues with the mechanical equipment can quickly be noticed, diagnosed, and replaced while the redundant backups take over if your system was sized correctly. You may still want a service contract unless your maintenance team is particularly handy, but they probably won’t be onsite as often.

### Overall 👍

If you’ve got the budget to go with a (significantly) more expensive upfront cost, this will probably be a better solution for you in the long run. Installing 6” piping mains through a historic schoolhouse won’t be cheap, but it will keep your students more comfortable and the mold at bay. Some providers may offer a loan or payment plan to help pay for the upgrades against your expected energy savings.

## Solution #3: VAV Air Handling Units

Whoa, this centralization concept is super cool - more efficiency, more redundancy, more control. How much of this stuff can we centralize? We’ve got the fan, filters, and coils, how about we throw them all in a box and duct the air out everywhere it needs to go?

Well, if you’ve got a nice mechanical mezzanine somewhere, or maybe a classroom you’re not using, sure we can do that. This big box will act just like the individual unit ventilators we described in the last section, but 15-30 times larger (and serve 15-30 more rooms). No more exterior louvers under every window!

### Temperature ✅

When only one room needs cooling, we just kick on the fan, bring in a little bit of outside air and little bit of return air from the space, and open the cooling coil little bit. The cold water from our chiller will cool down the air, then we can push it out into our ductwork.

How do we make sure that air gets to the right room? Well, each branch of duct will need to have a little damper, so we can direct the air to the space that requested it.

What if some spaces want hot air and some spaces want cold air? Well, we could run the cooling coil, then reconfigure the ductwork and then run the heating coil, only letting air into the correct space each time. That may work, but it’s not the best solution. It turns out we may need to de-centralize a little bit.

Let’s put a little heating coil next to the control damper in each branch of duct. Now we can let the big air handler put out a nice cool baseline (probably around 55F) and let each room open up the damper and heating coil independently depending on what they need. Not perfect centralization, but close!

### Freeze Protection ✅

Since this is still based on hydronic (water) coils, we still need to worry about freezing. Any of the aforementioned strategies will still work here, but coil pumps tend to be the most common for air handler setups in my experience.

### Humidity 🎉

Astute readers may have noticed that I mentioned that the air handler discharge temperature would probably be around 55F, and that 55F air is usually the rule of thumb for pre-cooled air ready for dehumidification. This means that the air handler has already done all of the hard work for us, and all we have to do in each branch is warm it up a little.

Additionally, the maintenance guys will be happy that the condensate drain is in one place, and it’s large enough it shouldn’t get backed up anymore.

### Carbon Dioxide/Particulates/Odor ✅

I mentioned earlier that we didn’t need louvers under every window, but we will still need a few to serve the big air handler. Thankfully we can locate these facing an interior courtyard or parking lot and avoid damaging our historic facade. The fresh air will help us with the carbon dioxide and particulate matter just like before.

### Pressurization ✅

it wasn’t on our list before, but with a centralized solution like this we can control the building’s pressure. Have you ever tried to open a door and felt a suction holding it shut, or saw a door that was held open by an inch or so as air rushed out? Those are examples of poor building pressure - our goal is to keep the unconditioned outside air from leaking in through gaps and cracks in the exterior walls without blowing doors or windows open. In some facilities like hospitals or pathogen research labs, you may want each room to keep air from entering or exiting unless it passes through a filter.

Since we’ve got a few big fans here that supply air to the spaces, we can measure the pressure differential between the interior and exterior and modulate the fan speeds to keep it exactly where we want it. (I should note that this is technically possible with some of the previous solutions but quite tricky to implement in practice. Centralization helps significantly!)

### Energy/Cost/Maintenance ✅

There are a few solid wins with big air handlers, but most of the benefits are actually better suited to an application with lots of small rooms. You just have to pay for cooling once and the cost of each additional branch is quite low. When your demand is low, you can ramp down the fan speed so it runs more efficiently. That’s actually where the name comes from - Variable Air Volume. Your VAV air handler can serve a wide variety of spaces at once, only running when it’s needed, and the VAV terminal units will keep each room at its exact setpoint. And that’s why air handlers are perfect for…

### Overall 🖊️

Offices!

Nearly every school like this will have one VAV air handler, and that’s to serve the administration offices! You can use the same chillers and boilers that run your classroom ventilators to run your principal’s office, nurse’s clinic, and reception area even more efficiently.

Using large equipment like this strategically allows you to leverage their strengths in each situation and fall back to the simpler (or cheaper) option when the downsides can be mitigated elsewhere.

# What does it all mean?

Engineering is tricky! There’s no single best solution for basically any situation, everything is based on a dozen factors and the end result is often arbitrary. What matters is less often “how many kilowatt-hours you saved this month” and more often how the maintenance staff feel about the system, how comfortable the rooms are, and how long the equipment will last before it needs to be replaced (and how hard it’s going to be to do so).

Also if you read this and came up with a dozen questions like “why don’t you just…” and “what about…” then you’re either a mechanical engineer already or should look into becoming one.
