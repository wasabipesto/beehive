# Life as a Controls Subcontractor

You’re a controls subcontractor. Your job is to take everything the mechanical engineer has specified and make it work. You will usually work for the mechanical contractor who has promised in advance that you’ll be able to make it work. Here are some things you’ll have to do and questions you’ll have to ask.

# Development

Sometimes you’re a salesperson. Ideally you’d have time to learn everything there is to know about the job before you give a price, but there’s a thousand pages of specs and only two weeks before bids are due, plus you have five other projects to bid. So you figure out the most important details:

- What equipment is going to be installed by others that needs to be controlled?
- What equipment are we going to install and control?
- What existing equipment are we going to control?
- Who are the approved vendors for equipment and devices?
- What installation standards are specified?

If you’re lucky you’ll be invited to an onsite pre-bid meeting. The engineers, general contractors, and trades should be there. Everyone will be writing things down on their drawings and taking photos. You might want to look around or ask about:

- Who is going to do demolition? When? What can they demolish and what needs to remain?
- Where are your new control panels going to go? It doesn’t matter if they are shown on the drawings, confirm this and make sure the electricians know where it is.
- Is there an existing controls frontend? Does it need to be integrated into yours? Can you get a system export or backup?
- How are you going to get power and communication trunks around the space? Is anything fire rated? Who patches new holes in the ceiling/walls?
- If going through an existing space, what’s above the ceiling? How much room is there? Do the walls go all the way to the deck? Block walls or drywall? Is wiremold acceptable for stats?

Look for anything that the owner might expect to be part of the project that isn’t explicitly noted. If there are old pneumatics, seized dampers, busted VFDs, etc, bring those up and ask if they should be included. If they are, make sure they get included in a bid addendum! You don’t want to price yourself out by including things other vendors don’t.

# Estimating

Sometimes you’re the estimator. You open up your excel spreadsheet and start plugging in everything from the drawings and everything from your pre-bid walkthrough notes. If you’re fancy this might be a dedicated estimation webapp, but in the end it’s essentially a spreadsheet. You should look at:

- How much time will it take your engineer to put together install docs?
- What physical devices do you need to buy to control everything as specified?
- What software licenses do you need to buy for your frontend or integration suite?
- How much time will it take your electrician to install those?
- How much time will it take your technician to get it running?
- How much time will it take your project manager to wrangle everyone to actually get it done?
- How much time have you taken so far putting together this estimate?

After you have a base number, you should look at:

- For similar types of projects in the past, what unexpected incidents did we run into? How likely are they to pop up here?
- Have you had good experiences with this project team in the past? Are there recurring issues you can plan for now?
- Does this project span multiple years? How much will inflation impact your material or labor rates?
- Will you have good competition between subcontractors, or do you have to use one particular group?
- What are the known unknowns? Are there any big “I’ll get back to you about that”s from the engineer? Anything you were unable to get eyes on during the pre-bid?

You get a number at the end. You tack on your margin, contingency, and anything else you can think of. If you have time, you sleep on it and add everything you forgot the next day. You put it on your letterhead, copy in your standard exclusions, and shoot it over.

If your price is low, you get a call grilling you to make sure you had everything included. If you’re high, they act like your best friend and ask if you remembered how easy this project is going to be.

You wait, and eventually get a contract.

# Engineering

Sometimes you’re an engineer. The salesperson hands you the project and you shake your head. You divide the engineering bucket by your chargeout rate and find out you only have 20 hours, minus some for revisions and putting together closeout docs at the end.

You start by doing everything they did, but correctly this time. You find 5 heaters that weren’t on the schedule and 6 motorized dampers that were missed because they were marked as “active gravity dampers”. In general, you:

- Get set up on Procore or whatever coordination site the contractors use. Hopefully they have all of the equipment submittals you need there. Fire off some RFIs if they’re missing any.
- Work through the drawings page by page. Highlight everything that might be remotely relevant. Highlight empty spaces where you think there should be something. Find any discrepancies or ambiguities. Fire off some RFIs.
- Read the specs. Read the entirety of Division 23 and highlight everything that might be remotely relevant. Skim the rest. Control+F search for things that the engineer might try to sneak in another section. Find any discrepancies or ambiguities. Fire off some RFIs.
- Find the sequences. They might be in the specs, or they might not. They may not even exist. If you’re lucky the engineer actually read them before dropping them in your lap. If you’re really lucky they made some changes to make it fit this system. Find any discrepancies or ambiguities. Fire off some RFIs.
- Hopefully by now you have all the submittals. Read them all, and highlight everything that might be remotely relevant. Get the phone numbers for every equipment rep and call them with questions. Understand how every single component works, what it needs and what it gives you. Fire off some RFIs if the capabilities don’t meet spec.

Now with all that out of the way, you can start your _actual_ job.

- Are any controls going to be factory-mounted? If so, make sure they have your contact info. Send them how you want everything mounted and wired. Get a sales order number and get the material sent over.
- Size out your valves and dampers. Don’t go off the drawings, go off the submittals so you know what was actually purchased. If the approved submittals are significantly different you could submit an RFI… or just go with it. Ship the valves to your mechanical contractor and dampers to your sheet metal contractor.
- Grab an empty floorplan layout and mark where in the building everything is. If you don’t have an empty floorplan, RFI.
- Connect all of the dots. Some devices need an ethernet connection from a main switch. Some devices need 24V power from a transformer. Some devices need a BACnet MSTP connection from a field server. Think about how your electrician is going to connect all of these.
- For each mechanical system, grab a template (if you have one) and mark it up with this project’s peculiarities. Otherwise sketch from scratch. Figure out what controller to use based on the program and point count.
- Pick out your devices based on the equipment and project spec. How many actuators do you need per damper? Which temperature sensors do you need for each point? What’s the system design flow and pressure? What hardwired safeties are necessary?
- For every point, build out your wiring diagram. For most devices the basics will be simple but the specifics will be tricky. Make sure you include not only the terminations but also the dip switch settings, mounting location, and auxiliary devices.
- Print it out and review. Mark up anything unclear or ambiguous. Double-check your relay logic. Skim the specs and drawings again to make sure you captured everything. Revise. Wake up the next day and add everything that came to you in your dream.

# Logistics

Sometimes you’re logistics. You know how much everything costs, what’s shipping from where, what parts have been coming in slow because the factory is missing a bracket, what alternate suppliers charge in overhead, and how many controllers you have stashed on a shelf. Nobody ever asks you about this. They just want everything, now.

You go through the engineer’s drawing set and put together a spreadsheet of every part in every system, where you need to order it from and where it’s going.

- Find the cheapest place that will deliver within a reasonable timeframe. Sometimes you order from the factory direct, sometimes it goes through a drop-shipper. Sometimes the factory is backordered but you know a guy who gets your order prioritized. Sometimes you find it on ebay.
- Sometimes you can’t find that part anywhere, and when you ask why people mutter “supply chain”. You find a couple alternates and ask the engineer which they want.
- You send the enclosure, controller, and some other parts to your panel build shop. If you’re not busy you might even do this yourself. They ship the assembled panels back a few weeks later.
- The project manager asks you when everything will be ready. You check the tracking numbers for dozens of orders and pull a few items from the shelf if you have them.
- You print out the drawing set in a nice binder, if the electrician wants one. Despite everything ostensibly going through their iPads now, most still want hard copies.
- You generate checkout sheets, network risers, and floorplan graphics for the technician. The checkout sheets go in another binder with another copy of the drawings.
- When everything has arrived, you divvy everything up into boxes based on the building, unit, phase, mezzanine, or room. You label each box, include a parts list, and help the project manager load it into their truck.

# Project Management

Sometimes you’re the project manager. You have ten jobs going and four on deck. Schedules are a suggestion at best. You are the master juggler.

You have three to-do lists for every project:

### Proactive

These items are things that will save you headaches down the road.

- Get a copy of the project schedule and mark key points that you need to be aware of. Let the GC know what those points are and to let you know if anything changes those dates.
- See if you can get electricians in the space early. If it’s a school, spring break is usually great for this. You can usually knock out a good portion of the comm cable in one week.
- Get tags printed for all panels. Some places like them on the ceiling for VAV boxes and FCUs as well. Things look much more professional with a label.
- Go over all material with logistics after it's boxed. Triple-check it has what you have written down.
- Take a list of material you bring to the jobsite and go over it with the electrician. Find a secure area for high-value items - a locked room within the building, on site trailer that electrical has on site, etc.
- For every mechanical well or tap, tape the pipe in a good, accessible location with the well/tap size and device tag. Walk the area with the mechanical contractor and make sure they know what needs to be done.
- Make sure the mechanical contractor knows they should **never** disassemble a valve. If there's a problem with a valve, they check with you first. They shouldn't ever rotate a valve actuator or reconfigure a 3W butterfly valve.
- Check in with the electrician and get ethernet tip/test reports as soon as comm cable is done.

### Recurring

You make sure you check these every week. Make yourself known, and make yourself annoying if you see a problem.

- Attend progress meetings, in-person as often as possible. These meetings are where decisions get made and you should make your voice heard here.
- Check the progress of your electrician. Make sure they're covering the scope like you intended. Check things yourself and then have them walk you through it.
- Look out for mechanical contractors installing your valves. Make sure the valves are installed with the actuator between 3 and 9-oclock. Any lower and condensation will drip on the valve and shorten the life.
- Keep in contact with your subcontractor's foreman and coordinator. Let them know when work is coming up and find out how much manpower they have available. If they're not very busy, see if you can find work for them to get done early.
- Send project updates every single week, even if nothing is happening. Recap everything you are doing, everything your subcontractor has done, what you need from the PM, what you need from other contractors, what you're waiting on, what you're doing next week. If there's anything you see that could impact their schedule, bring it up every week and get it documented.

### Reactive

Things will come up unexpectedly. Little problems are just as important as big problems when maintaining trust.

- Minor questions and implementation details should immediately get routed to your control engineer. Loop in the general contractor if it requires coordination. Keep everyone updated until the item is resolved to everyone’s satisfaction.
- Big changes or strategy questions should still go through the control engineer to see if they already brought it up, but they will likely kick it up to the general contractors and project engineers. Make sure a drawing revision with accurate information is passed along to the electricians when the final strategy is accepted.
- Redlines from your subcontractor, another contractor, or your technician need to be saved for closeout documents. If you notice deviations that were not captured in redlines, mark it yourself and make sure nothing else was missed.

If you're lucky, and everything goes well, and everyone does their job right, then you get to go home.
