# Chapter 21 - Circuits and DC Instruments

  
FIGURE 21.1 Electric circuits in computers and servers allow large amounts of data to be quickly and accurately analyzed. (credit: WOCinTech Chat/Flickr)

# CHAPTER OUTLINE

21.1 Resistors in Series and Parallel   
21.2 Electromotive Force: Terminal Voltage   
21.3 Kirchhoff’s Rules   
21.4 DC Voltmeters and Ammeters   
21.5 Null Measurements   
21.6 DC Circuits Containing Resistors and Capacitors

INTRODUCTION TO CIRCUITS AND DC INSTRUMENTS Electric circuits are commonplace. Some are simple, such as those in flashlights. Others, such as those used in supercomputers, are extremely complex.

This collection of modules takes the topic of electric circuits a step beyond simple circuits. When the circuit is purely resistive, everything in this module applies to both DC and AC. Matters become more complex when capacitance is involved. We do consider what happens when capacitors are connected to DC voltage sources, but the interaction of capacitors and other nonresistive devices with AC is left for a later chapter. Finally, a number of important DC instruments, such as meters that measure voltage and current, are covered in this chapter.# 21.1 Resistors in Series and Parallel

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Draw a circuit with resistors in parallel and in series.   
Calculate the voltage drop of a current across a resistor using Ohm’s law.   
Contrast the way total resistance is calculated for resistors in series and in parallel.   
Explain why total resistance of a parallel circuit is less than the smallest resistance of any of the resistors in that circuit.   
Calculate total resistance of a circuit that contains a mixture of resistors connected in series and in parallel.

Most circuits have more than one component, called a resistor that limits the flow of charge in the circuit. A measure of this limit on charge flow is called resistance. The simplest combinations of resistors are the series and parallel connections illustrated in Figure 21.2. The total resistance of a combination of resistors depends on both their individual values and how they are connected.

  
FIGURE 21.2 (a) A series connection of resistors. (b) A parallel connection of resistors.

# Resistors in Series

When are resistors in series? Resistors are in series whenever the flow of charge, called the current, must flow through devices sequentially. For example, if current flows through a person holding a screwdriver and into the Earth, then  in Figure 21.2(a) could be the resistance of the screwdriver’s shaft,  the resistance of its handle,  the person’s body resistance, and  the resistance of her shoes.

Figure 21.3 shows resistors in series connected to a voltage source. It seems reasonable that the total resistance is the sum of the individual resistances, considering that the current has to pass through each resistor in sequence. (This fact would be an advantage to a person wishing to avoid an electrical shock, who could reduce the current by wearing high-resistance rubber-soled shoes. It could be a disadvantage if one of the resistances were a faulty highresistance cord to an appliance that would reduce the operating current.)

  
FIGURE 21.3 Three resistors connected in series to a battery (left) and the equivalent single or series resistance (right).

To verify that resistances in series do indeed add, let us consider the loss of electrical power, called a voltage drop, in each resistor in Figure 21.3.

According to Ohm’s law, the voltage drop,  , across a resistor when a current flows through it is calculated using the equation  , where  equals the current in amps (A) and  is the resistance in ohms  . Another way tothink of this is that  is the voltage necessary to make a current  flow through a resistance  .

So the voltage drop across  is  , that across  is  , and that across  is  . The sum of these voltages equals the voltage output of the source; that is,



This equation is based on the conservation of energy and conservation of charge. Electrical potential energy can be described by the equation  where  is the electric charge and  is the voltage. Thus the energy supplied by the source is  while that dissipated by the resistors is



# Connections: Conservation Laws

The derivations of the expressions for series and parallel resistance are based on the laws of conservation of energy and conservation of charge, which state that total charge and total energy are constant in any process. These two laws are directly involved in all electrical phenomena and will be invoked repeatedly to explain both specific effects and the general behavior of electricity.

These energies must be equal, because there is no other source and no other destination for energy in the circuit. Thus,  . The charge  cancels, yielding  , as stated. (Note that the same amount of charge passes through the battery and each resistor in a given amount of time, since there is no capacitance to store charge, there is no place for charge to leak, and charge is conserved.)

Now substituting the values for the individual voltages gives



Note that for the equivalent single series resistance  , we have



This implies that the total or equivalent series resistance  of three resistors is  .

This logic is valid in general for any number of resistors in series; thus, the total resistance  of a series connection is



as proposed. Since all of the current must pass through each resistor, it experiences the resistance of each, and resistances in series simply add up.

# EXAMPLE 21.1

# Calculating Resistance, Current, Voltage Drop, and Power Dissipation: Analysis of a Series Circuit

Suppose the voltage output of the battery in Figure 21.3 is  , and the resistances are  ,  , and  . (a) What is the total resistance? (b) Find the current. (c) Calculate the voltage drop in each resistor, and show these add to equal the voltage output of the source. (d) Calculate the power dissipated by each resistor. (e) Find the power output of the source, and show that it equals the total power dissipated by the resistors.

# Strategy and Solution for (a)

The total resistance is simply the sum of the individual resistances, as given by this equation:

# Strategy and Solution for (b)

The current is found using Ohm’s law,  . Entering the value of the applied voltage and the total resistance yields the current for the circuit:



# Strategy and Solution for (c)

The voltage—or  drop—in a resistor is given by Ohm’s law. Entering the current and the value of the first resistance yields



Similarly,



and



# Discussion for (c)

The three  drops add to  , as predicted:



# Strategy and Solution for (d)

The easiest way to calculate power in watts (W) dissipated by a resistor in a DC circuit is to use Joule’s law,  where  is electric power. In this case, each resistor has the same full current flowing through it. By substituting Ohm’s law  into Joule’s law, we get the power dissipated by the first resistor as



Similarly,



and



# Discussion for (d)

Power can also be calculated using either  , where is the voltage drop across the resistor (not the full voltage of the source). The same values will be obtained.

# Strategy and Solution for (e)

The easiest way to calculate power output of the source is to use  where  is the source voltage. This gives



# Discussion for (e)

Note, coincidentally, that the total power dissipated by the resistors is also 7.20 W, the same as the power put out by the source. That is,



Power is energy per unit time (watts), and so conservation of energy requires the power output of the source to be equal to the total power dissipated by the resistors.# Major Features of Resistors in Series

1. Series resistances add:    
2. The same current flows through each resistor in series.   
3. Individual resistors in series do not get the total source voltage, but divide it.

# Resistors in Parallel

Figure 21.4 shows resistors in parallel, wired to a voltage source. Resistors are in parallel when each resistor is connected directly to the voltage source by connecting wires having negligible resistance. Each resistor thus has the full voltage of the source applied to it.

Each resistor draws the same current it would if it alone were connected to the voltage source (provided the voltage source is not overloaded). For example, an automobile’s headlights, radio, and so on, are wired in parallel, so that they utilize the full voltage of the source and can operate completely independently. The same is true in your house, or any building. (See Figure 21.4(b).)

  
FIGURE 21.4 (a) Three resistors connected in parallel to a battery and the equivalent single or parallel resistance. (b) Electrical power setup in a house. (credit: Dmitry G, Wikimedia Commons)

To find an expression for the equivalent parallel resistance  , let us consider the currents that flow and how they are related to resistance. Since each resistor in the circuit has the full voltage, the currents flowing through the individual resistors are  . , and  . Conservation of charge implies that the total current  produced by the source is the sum of these currents:

Substituting the expressions for the individual currents gives



Note that Ohm’s law for the equivalent single resistance gives



The terms inside the parentheses in the last two equations must be equal. Generalizing to any number of resistors, the total resistance  of a parallel connection is related to the individual resistances by



This relationship results in a total resistance  that is less than the smallest of the individual resistances. (This is seen in the next example.) When resistors are connected in parallel, more current flows from the source than would flow for any of them individually, and so the total resistance is lower.

# EXAMPLE 21.2

# Calculating Resistance, Current, Power Dissipation, and Power Output: Analysis of a Parallel Circuit

Let the voltage output of the battery and resistances in the parallel connection in Figure 21.4 be the same as the previously considered series connection:  ,  ,  , and  . (a) What is the total resistance? (b) Find the total current. (c) Calculate the currents in each resistor, and show these add to equal the total current output of the source. (d) Calculate the power dissipated by each resistor. (e) Find the power output of the source, and show that it equals the total power dissipated by the resistors.

# Strategy and Solution for (a)

The total resistance for a parallel combination of resistors is found using the equation below. Entering known values gives



Thus,



(Note that in these calculations, each intermediate answer is shown with an extra digit.)

We must invert this to find the total resistance  . This yields



The total resistance with the correct number of significant digits is 

# Discussion for (a)

 is, as predicted, less than the smallest individual resistance.

# Strategy and Solution for (b)

The total current can be found from Ohm’s law, substituting  for the total resistance. This gives

# Discussion for (b)

Current  for each device is much larger than for the same devices connected in series (see the previous example). A circuit with parallel connections has a smaller total resistance than the resistors connected in series.

# Strategy and Solution for (c)

The individual currents are easily calculated from Ohm’s law, since each resistor gets the full voltage. Thus,



Similarly,



and



# Discussion for (c)

The total current is the sum of the individual currents:



This is consistent with conservation of charge.

# Strategy and Solution for (d)

The power dissipated by each resistor can be found using any of the equations relating power to current, voltage, and resistance, since all three are known. Let us use  , since each resistor gets full voltage. Thus,



Similarly,



and



# Discussion for (d)

The power dissipated by each resistor is considerably higher in parallel than when connected in series to the same voltage source.

# Strategy and Solution for (e)

The total power can also be calculated in several ways. Choosing  and entering the total current, yields



# Discussion for (e)

Total power dissipated by the resistors is also 179 W:

This is consistent with the law of conservation of energy.

# Overall Discussion

Note that both the currents and powers in parallel connections are greater than for the same devices in series.

# Major Features of Resistors in Parallel

1. Parallel resistance is found from  and it is smaller than any individual resistance in the combination.   
2. Each resistor in parallel has the same full voltage of the source applied to it. (Power distribution systems most often use parallel connections to supply the myriad devices served with the same voltage and to allow them to operate independently.)   
3. Parallel resistors do not each get the total current; they divide it.

# Combinations of Series and Parallel

More complex connections of resistors are sometimes just combinations of series and parallel. These are commonly encountered, especially when wire resistance is considered. In that case, wire resistance is in series with other resistances that are in parallel.

Combinations of series and parallel can be reduced to a single equivalent resistance using the technique illustrated in Figure 21.5. Various parts are identified as either series or parallel, reduced to their equivalents, and further reduced until a single resistance is left. The process is more time consuming than difficult.

  
FIGURE 21.5 This combination of seven resistors has both series and parallel parts. Each is identified and reduced to an equivalent resistance, and these are further reduced until a single equivalent resistance is reached.

The simplest combination of series and parallel resistance, shown in Figure 21.6, is also the most instructive, since it is found in many applications. For example,  could be the resistance of wires from a car battery to its electrical devices, which are in parallel.  and  could be the starter motor and a passenger compartment light. We have previously assumed that wire resistance is negligible, but, when it is not, it has important effects, as the next example indicates.# EXAMPLE 21.3

# Calculating Resistance,  Drop, Current, and Power Dissipation: Combining Series and Parallel Circuits

Figure  shows the resistors from the previous two examples wired in a different way—a combination of series and parallel. We can consider  to be the resistance of wires leading to  and  . (a) Find the total resistance. (b) What is the  drop in  (c) Find the current  through  . (d) What power is dissipated by  ?

  
FIGURE 21.6 These three resistors are connected to a voltage source so that  and  are in parallel with one another and that combination is in series with  .

# Strategy and Solution for (a)

To find the total resistance, we note that  and  are in parallel and their combination  is in series with  . Thus the total (equivalent) resistance of this combination is



First, we find  using the equation for resistors in parallel and entering known values:



Inverting gives



So the total resistance is



# Discussion for (a)

The total resistance of this combination is intermediate between the pure series and pure parallel values  and  , respectively) found for the same resistors in the two previous examples.

# Strategy and Solution for (b)

To find the  drop in  , we note that the full current  flows through  . Thus its  drop is



We must find  before we can calculate  . The total current  is found using Ohm’s law for the circuit. That is,



Entering this into the expression above, we get

# Discussion for (b)

The voltage applied to  and  is less than the total voltage by an amount  . When wire resistance is large, it can significantly affect the operation of the devices represented by  and  .

# Strategy and Solution for (c)

To find the current through  , we must first find the voltage applied to it. We call this voltage  , because it is applied to a parallel combination of resistors. The voltage applied to both  and  is reduced by the amount  , and so it is



Now the current  through resistance  is found using Ohm’s law:



# Discussion for (c)

The current is less than the 2.00 A that flowed through  when it was connected in parallel to the battery in the previous parallel circuit example.

# Strategy and Solution for (d)

The power dissipated by  is given by



# Discussion for (d)

The power is less than the 24.0 W this resistor dissipated when connected in parallel to the 12.0-V source.

# Practical Implications

One implication of this last example is that resistance in wires reduces the current and power delivered to a resistor. If wire resistance is relatively large, as in a worn (or a very long) extension cord, then this loss can be significant. If a large current is drawn, the  drop in the wires can also be significant.

For example, when you are rummaging in the refrigerator and the motor comes on, the refrigerator light dims momentarily. Similarly, you can see the passenger compartment light dim when you start the engine of your car (although this may be due to resistance inside the battery itself).

What is happening in these high-current situations is illustrated in Figure 21.7. The device represented by  has a very low resistance, and so when it is switched on, a large current flows. This increased current causes a larger  drop in the wires represented by  , reducing the voltage across the light bulb (which is  ), which then dims noticeably.  
FIGURE 21.7 Why do lights dim when a large appliance is switched on? The answer is that the large current the appliance motor draws causes a significant  drop in the wires and reduces the voltage across the light.

# CHECK YOUR UNDERSTANDING

Can any arbitrary combination of resistors be broken down into series and parallel combinations? See if you can draw a circuit diagram of resistors that cannot be broken down into combinations of series and parallel.

# Solution

No, there are many ways to connect resistors that are not combinations of series and parallel, including loops and junctions. In such cases Kirchhoff’s rules, to be introduced in Kirchhoff’s Rules, will allow you to analyze the circuit.

# Problem-Solving Strategies for Series and Parallel Resistors

1. Draw a clear circuit diagram, labeling all resistors and voltage sources. This step includes a list of the knowns for the problem, since they are labeled in your circuit diagram.   
2. Identify exactly what needs to be determined in the problem (identify the unknowns). A written list is useful.   
3. Determine whether resistors are in series, parallel, or a combination of both series and parallel. Examine the circuit diagram to make this assessment. Resistors are in series if the same current must pass sequentially through them.   
4. Use the appropriate list of major features for series or parallel connections to solve for the unknowns. There is one list for series and another for parallel. If your problem has a combination of series and parallel, reduce it in steps by considering individual groups of series or parallel connections, as done in this module and the examples. Special note: When finding  , the reciprocal must be taken with care.   
5. Check to see whether the answers are reasonable and consistent. Units and numerical results must be reasonable. Total series resistance should be greater, whereas total parallel resistance should be smaller, for example. Power should be greater for the same devices in parallel compared with series, and so on.

# 21.2 Electromotive Force: Terminal Voltage

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Compare and contrast the voltage and the electromagnetic force of an electric power source. Describe what happens to the terminal voltage, current, and power delivered to a load as internal resistance of the voltage source increases (due to aging of batteries, for example). Explain why it is beneficial to use more than one voltage source connected in parallel.

When you forget to turn off your car lights, they slowly dim as the battery runs down. Why don’t they simply blink off when the battery’s energy is gone? Their gradual dimming implies that battery output voltage decreases as the battery is depleted.Furthermore, if you connect an excessive number of 12-V lights in parallel to a car battery, they will be dim even when the battery is fresh and even if the wires to the lights have very low resistance. This implies that the battery’s output voltage is reduced by the overload.

The reason for the decrease in output voltage for depleted or overloaded batteries is that all voltage sources have two fundamental parts—a source of electrical energy and an internal resistance. Let us examine both.

# Electromotive Force

You can think of many different types of voltage sources. Batteries themselves come in many varieties. There are many types of mechanical/electrical generators, driven by many different energy sources, ranging from nuclear to wind. Solar cells create voltages directly from light, while thermoelectric devices create voltage from temperature differences.

A few voltage sources are shown in Figure 21.8. All such devices create a potential difference and can supply current if connected to a resistance. On the small scale, the potential difference creates an electric field that exerts force on charges, causing current. We thus use the name electromotive force, abbreviated emf.

Emf is not a force at all; it is a special type of potential difference. To be precise, the electromotive force (emf) is the potential difference of a source when no current is flowing. Units of emf are volts.

  
FIGURE 21.8 A variety of voltage sources (clockwise from top left): the Brazos Wind Farm in Fluvanna, Texas (credit: Leaflet, Wikimedia Commons); the Krasnoyarsk Dam in Russia (credit: Alex Polezhaev); a solar farm (credit: U.S. Department of Energy); and a group of nickel metal hydride batteries (credit: Tiaa Monto). The voltage output of each depends on its construction and load, and equals emf only if there is no load.

Electromotive force is directly related to the source of potential difference, such as the particular combination of chemicals in a battery. However, emf differs from the voltage output of the device when current flows. The voltage across the terminals of a battery, for example, is less than the emf when the battery supplies current, and it declines further as the battery is depleted or loaded down. However, if the device’s output voltage can be measured without drawing current, then output voltage will equal emf (even for a very depleted battery).

# Internal Resistance

As noted before, a 12-V truck battery is physically larger, contains more charge and energy, and can deliver a larger current than a 12-V motorcycle battery. Both are lead-acid batteries with identical emf, but, because of its size, the truck battery has a smaller internal resistance  . Internal resistance is the inherent resistance to the flow of current within the source itself.

Figure 21.9 is a schematic representation of the two fundamental parts of any voltage source. The emf (represented by a script E in the figure) and internal resistance  are in series. The smaller the internal resistance for a given emf, the more current and the more power the source can supply.  
FIGURE 21.9 Any voltage source (in this case, a carbon-zinc dry cell) has an emf related to its source of potential difference, and an internal resistance  related to its construction. (Note that the script E stands for emf.). Also shown are the output terminals across which the terminal voltage  is measured. Since  , terminal voltage equals emf only if there is no current flowing.

The internal resistance  can behave in complex ways. As noted,  increases as a battery is depleted. But internal resistance may also depend on the magnitude and direction of the current through a voltage source, its temperature, and even its history. The internal resistance of rechargeable nickel-cadmium cells, for example, depends on how many times and how deeply they have been depleted.

# Things Great and Small: The Submicroscopic Origin of Battery Potential

Various types of batteries are available, with emfs determined by the combination of chemicals involved. We can view this as a molecular reaction (what much of chemistry is about) that separates charge.

The lead-acid battery used in cars and other vehicles is one of the most common types. A single cell (one of six) of this battery is seen in Figure 21.10. The cathode (positive) terminal of the cell is connected to a lead oxide plate, while the anode (negative) terminal is connected to a lead plate. Both plates are immersed in sulfuric acid, the electrolyte for the system.

  
FIGURE 21.10 Artist’s conception of a lead-acid cell. Chemical reactions in a lead-acid cell separate charge, sending negative charge to the anode, which is connected to the lead plates. The lead oxide plates are connected to the positive or cathode terminal of the cell. Sulfuric acid conducts the charge as well as participating in the chemical reaction.

The details of the chemical reaction are left to the reader to pursue in a chemistry text, but their results at the molecular level help explain the potential created by the battery. Figure 21.11 shows the result of a single chemical reaction. Two electrons are placed on the anode, making it negative, provided that the cathode supplied two electrons. This leaves the cathode positively charged, because it has lost two electrons. In short, a separation of charge has been driven by a chemical reaction.

Note that the reaction will not take place unless there is a complete circuit to allow two electrons to be supplied to the cathode. Under many circumstances, these electrons come from the anode, flow through a resistance, and return to the cathode. Note also that since the chemical reactions involve substances with resistance, it is not possible to create the emf without an internal resistance.  
FIGURE 21.11 Artist’s conception of two electrons being forced onto the anode of a cell and two electrons being removed from the cathode of the cell. The chemical reaction in a lead-acid battery places two electrons on the anode and removes two from the cathode. It requires a closed circuit to proceed, since the two electrons must be supplied to the cathode.

Why are the chemicals able to produce a unique potential difference? Quantum mechanical descriptions of molecules, which take into account the types of atoms and numbers of electrons in them, are able to predict the energy states they can have and the energies of reactions between them.

In the case of a lead-acid battery, an energy of  is given to each electron sent to the anode. Voltage is defined as the electrical potential energy divided by charge:  . An electron volt is the energy given to a single electron by a voltage of 1 V. So the voltage here is  , since  is given to each electron. It is the energy produced in each molecular reaction that produces the voltage. A different reaction produces a different energy and, hence, a different voltage.

# Terminal Voltage

The voltage output of a device is measured across its terminals and, thus, is called its terminal voltage . Terminal voltage is given by



where  is the internal resistance and  is the current flowing at the time of the measurement.

 is positive if current flows away from the positive terminal, as shown in Figure 21.9. You can see that the larger the current, the smaller the terminal voltage. And it is likewise true that the larger the internal resistance, the smaller the terminal voltage.

Suppose a load resistance  is connected to a voltage source, as in Figure 21.12. Since the resistances are in series, the total resistance in the circuit is  . Thus the current is given by Ohm’s law to be

  
FIGURE 21.12 Schematic of a voltage source and its load  . Since the internal resistance  is in series with the load, it can significantly affect the terminal voltage and current delivered to the load. (Note that the script E stands for emf.)

We see from this expression that the smaller the internal resistance  , the greater the current the voltage source supplies to its load  . As batteries are depleted,  increases. If  becomes a significant fraction of the load resistance, then the current is significantly reduced, as the following example illustrates.# Calculating Terminal Voltage, Power Dissipation, Current, and Resistance: Terminal Voltage and Load

A certain battery has a 12.0-V emf and an internal resistance of  . (a) Calculate its terminal voltage when connected to a load. (b) What is the terminal voltage when connected to a load? (c) What power does the  load dissipate? (d) If the internal resistance grows to  , find the current, terminal voltage, and power dissipated by a load.

# Strategy

The analysis above gave an expression for current when internal resistance is taken into account. Once the current is found, the terminal voltage can be calculated using the equation  . Once current is found, the power dissipated by a resistor can also be found.

# Solution for (a)

Entering the given values for the emf, load resistance, and internal resistance into the expression above yields



Enter the known values into the equation  to get the terminal voltage:



# Discussion for (a)

The terminal voltage here is only slightly lower than the emf, implying that  is a light load for this particular battery.

# Solution for (b)

Similarly, with  , the current is



The terminal voltage is now



# Discussion for (b)

This terminal voltage exhibits a more significant reduction compared with emf, implying  is a heavy load for this battery.

# Solution for (c)

The power dissipated by the  load can be found using the formula  . Entering the known values gives



# Discussion for (c)

Note that this power can also be obtained using the expressions  or  where  is the terminal voltage (10.0 V in this case).# Solution for (d)

Here the internal resistance has increased, perhaps due to the depletion of the battery, to the point where it is as great as the load resistance. As before, we first find the current by entering the known values into the expression, yielding



Now the terminal voltage is



and the power dissipated by the load is



# Discussion for (d)

We see that the increased internal resistance has significantly decreased terminal voltage, current, and power delivered to a load.

Battery testers, such as those in Figure 21.13, use small load resistors to intentionally draw current to determine whether the terminal voltage drops below an acceptable level. They really test the internal resistance of the battery. If internal resistance is high, the battery is weak, as evidenced by its low terminal voltage.

  
FIGURE 21.13 These two battery testers measure terminal voltage under a load to determine the condition of a battery. The large device is being used by a U.S. Navy electronics technician to test large batteries aboard the aircraft carrier USS Nimitz and has a small resistance that can dissipate large amounts of power. (credit: U.S. Navy photo by Photographer’s Mate Airman Jason A. Johnston) The small device is used on small batteries and has a digital display to indicate the acceptability of their terminal voltage. (credit: Keith Williamson)

Some batteries can be recharged by passing a current through them in the direction opposite to the current they supply to a resistance. This is done routinely in cars and batteries for small electrical appliances and electronic devices, and is represented pictorially in Figure 21.14. The voltage output of the battery charger must be greater than the emf of the battery to reverse current through it. This will cause the terminal voltage of the battery to be greater than the emf, since  , and  is now negative.

  
FIGURE 21.14 A car battery charger reverses the normal direction of current through a battery, reversing its chemical reaction and replenishing its chemical potential.

# Multiple Voltage Sources

There are two voltage sources when a battery charger is used. Voltage sources connected in series are relatively simple. When voltage sources are in series, their internal resistances add and their emfs add algebraically. (SeeFigure 21.15.) Series connections of voltage sources are common—for example, in flashlights, toys, and other appliances. Usually, the cells are in series in order to produce a larger total emf.

But if the cells oppose one another, such as when one is put into an appliance backward, the total emf is less, since it is the algebraic sum of the individual emfs.

A battery is a multiple connection of voltaic cells, as shown in Figure 21.16. The disadvantage of series connections of cells is that their internal resistances add. One of the authors once owned a 1957 MGA that had two 6-V batteries in series, rather than a single 12-V battery. This arrangement produced a large internal resistance that caused him many problems in starting the engine.

  
FIGURE 21.15 A series connection of two voltage sources. The emfs (each labeled with a script E) and internal resistances add, giving a total emf of  and a total internal resistance of  .

  
FIGURE 21.16 Batteries are multiple connections of individual cells, as shown in this modern rendition of an old print. Single cells, such as AA or C cells, are commonly called batteries, although this is technically incorrect.

If the series connection of two voltage sources is made into a complete circuit with the emfs in opposition, then a current of magnitude  flows. See Figure 21.17, for example, which shows a circuit exactly analogous to the battery charger discussed above. If two voltage sources in series with emfs in the same sense are connected to a load  , as in Figure 21.18, then  flows.

  
FIGURE 21.17 These two voltage sources are connected in series with their emfs in opposition. Current flows in the direction of the greater emf and is limited to  by the sum of the internal resistances. (Note that each emf is represented by script E in the figure.) A battery charger connected to a battery is an example of such a connection. The charger must have a larger emf than the battery to reverse current through it.  
FIGURE 21.18 This schematic represents a flashlight with two cells (voltage sources) and a single bulb (load resistance) in series. The current that flows is  . (Note that each emf is represented by script E in the figure.)

# Take-Home Experiment: Flashlight Batteries

Find a flashlight that uses several batteries and find new and old batteries. Based on the discussions in this module, predict the brightness of the flashlight when different combinations of batteries are used. Do your predictions match what you observe? Now place new batteries in the flashlight and leave the flashlight switched on for several hours. Is the flashlight still quite bright? Do the same with the old batteries. Is the flashlight as bright when left on for the same length of time with old and new batteries? What does this say for the case when you are limited in the number of available new batteries?

Figure 21.19 shows two voltage sources with identical emfs in parallel and connected to a load resistance. In this simple case, the total emf is the same as the individual emfs. But the total internal resistance is reduced, since the internal resistances are in parallel. The parallel connection thus can produce a larger current.

Here,  flows through the load, and  is less than those of the individual batteries. For example, some diesel-powered cars use two  batteries in parallel; they produce a total emf of  but can deliver the larger current needed to start a diesel engine.

  
FIGURE 21.19 Two voltage sources with identical emfs (each labeled by script E) connected in parallel produce the same emf but have a smaller total internal resistance than the individual sources. Parallel combinations are often used to deliver more current. Here  flows through the load.

# Animals as Electrical Detectors

A number of animals both produce and detect electrical signals. Fish, sharks, platypuses, and echidnas (spiny anteaters) all detect electric fields generated by nerve activity in prey. Electric eels produce their own emf through biological cells (electric organs) called electroplaques, which are arranged in both series and parallel as a set of batteries.

Electroplaques are flat, disk-like cells; those of the electric eel have a voltage of 0.15 V across each one. These cellsare usually located toward the head or tail of the animal, although in the case of the electric eel, they are found along the entire body. The electroplaques in the South American eel are arranged in 140 rows, with each row stretching horizontally along the body and containing 5,000 electroplaques. This can yield an emf of approximately 600 V, and a current of 1 A—deadly.

The mechanism for detection of external electric fields is similar to that for producing nerve signals in the cell through depolarization and repolarization—the movement of ions across the cell membrane. Within the fish, weak electric fields in the water produce a current in a gel-filled canal that runs from the skin to sensing cells, producing a nerve signal. The Australian platypus, one of the very few mammals that lay eggs, can detect fields of 30 , while sharks have been found to be able to sense a field in their snouts as small as 100 (Figure 21.20). Electric eels use their own electric fields produced by the electroplaques to stun their prey or enemies.

  
FIGURE 21.20 Sand tiger sharks (Carcharias taurus), like this one at the Minnesota Zoo, use electroreceptors in their snouts to locate prey. (credit: Jim Winstead, Flickr)

# Solar Cell Arrays

Another example dealing with multiple voltage sources is that of combinations of solar cells—wired in both series and parallel combinations to yield a desired voltage and current. Photovoltaic generation (PV), the conversion of sunlight directly into electricity, is based upon the photoelectric effect, in which photons hitting the surface of a solar cell create an electric current in the cell.

Most solar cells are made from pure silicon—either as single-crystal silicon, or as a thin film of silicon deposited upon a glass or metal backing. Most single cells have a voltage output of about 0.5 V, while the current output is a function of the amount of sunlight upon the cell (the incident solar radiation—the insolation). Under bright noon sunlight, a current of about  of cell surface area is produced by typical single-crystal cells.

Individual solar cells are connected electrically in modules to meet electrical-energy needs. They can be wired together in series or in parallel—connected like the batteries discussed earlier. A solar-cell array or module usually consists of between 36 and 72 cells, with a power output of 50 W to 140 W.

The output of the solar cells is direct current. For most uses in a home, AC is required, so a device called an inverter must be used to convert the DC to AC. Any extra output can then be passed on to the outside electrical grid for sale to the utility.

# Take-Home Experiment: Virtual Solar Cells

One can assemble a “virtual” solar cell array by using playing cards, or business or index cards, to represent a solar cell. Combinations of these cards in series and/or parallel can model the required array output. Assume each card has an output of  and a current (under bright light) of 2 A. Using your cards, how would youarrange them to produce an output of 6 A at 3 V (18 W)?

Suppose you were told that you needed only 18 W (but no required voltage). Would you need more cards to make this arrangement?

# 21.3 Kirchhoff’s Rules

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Analyze a complex circuit using Kirchhoff’s rules, using the conventions for determining the correct signs of various terms.

Many complex circuits, such as the one in Figure 21.21, cannot be analyzed with the series-parallel techniques developed in Resistors in Series and Parallel and Electromotive Force: Terminal Voltage. There are, however, two circuit analysis rules that can be used to analyze any circuit, simple or complex. These rules are special cases of the laws of conservation of charge and conservation of energy. The rules are known as Kirchhoff’s rules, after their inventor Gustav Kirchhoff (1824–1887).

  
FIGURE 21.21 This circuit cannot be reduced to a combination of series and parallel connections. Kirchhoff’s rules, special applications of the laws of conservation of charge and energy, can be used to analyze it. (Note: The script E in the figure represents electromotive force, emf.)

# Kirchhoff’s Rules

• Kirchhoff’s first rule—the junction rule. The sum of all currents entering a junction must equal the sum of all currents leaving the junction. Kirchhoff’s second rule—the loop rule. The algebraic sum of changes in potential around any closed circuit path (loop) must be zero.

Explanations of the two rules will now be given, followed by problem-solving hints for applying Kirchhoff’s rules, and a worked example that uses them.

# Kirchhoff’s First Rule

Kirchhoff’s first rule (the junction rule) is an application of the conservation of charge to a junction; it is illustrated in Figure 21.22. Current is the flow of charge, and charge is conserved; thus, whatever charge flows into the junction must flow out. Kirchhoff’s first rule requires that  (see figure). Equations like this can and will be used to analyze circuits and to solve circuit problems.# Making Connections: Conservation Laws

Kirchhoff’s rules for circuit analysis are applications of conservation laws to circuits. The first rule is the application of conservation of charge, while the second rule is the application of conservation of energy. Conservation laws, even used in a specific application, such as circuit analysis, are so basic as to form the foundation of that application.



  
FIGURE 21.22 The junction rule. The diagram shows an example of Kirchhoff’s first rule where the sum of the currents into a junction equals the sum of the currents out of a junction. In this case, the current going into the junction splits and comes out as two currents, so that  . Here  must be  , since  is  and  is  .

# Kirchhoff’s Second Rule

Kirchhoff’s second rule (the loop rule) is an application of conservation of energy. The loop rule is stated in terms of potential,  , rather than potential energy, but the two are related since  Recall that emf is the potential difference of a source when no current is flowing. In a closed loop, whatever energy is supplied by emf must be transferred into other forms by devices in the loop, since there are no other ways in which energy can be transferred into or out of the circuit. Figure 21.23 illustrates the changes in potential in a simple series circuit loop.

Kirchhoff’s second rule requires  . Rearranged, this is  , which means the emf equals the sum of the  (voltage) drops in the loop.

  
FIGURE 21.23 The loop rule. An example of Kirchhoff’s second rule where the sum of the changes in potential around a closed loop must be zero. (a) In this standard schematic of a simple series circuit, the emf supplies  , which is reduced to zero by the resistances, with 1 Vacross the internal resistance, and  and 5 V across the two load resistances, for a total of 18 V. (b) This perspective view represents the potential as something like a roller coaster, where charge is raised in potential by the emf and lowered by the resistances. (Note that the script E stands for emf.)

# Applying Kirchhoff’s Rules

By applying Kirchhoff’s rules, we generate equations that allow us to find the unknowns in circuits. The unknowns may be currents, emfs, or resistances. Each time a rule is applied, an equation is produced. If there are as many independent equations as unknowns, then the problem can be solved. There are two decisions you must make when applying Kirchhoff’s rules. These decisions determine the signs of various quantities in the equations you obtain from applying the rules.

1. When applying Kirchhoff’s first rule, the junction rule, you must label the current in each branch and decide in what direction it is going. For example, in Figure 21.21, Figure 21.22, and Figure 21.23, currents are labeled  ,  , and  , and arrows indicate their directions. There is no risk here, for if you choose the wrong direction, the current will be of the correct magnitude but negative.

2. When applying Kirchhoff’s second rule, the loop rule, you must identify a closed loop and decide in which direction to go around it, clockwise or counterclockwise. For example, in Figure 21.23 the loop was traversed in the same direction as the current (clockwise). Again, there is no risk; going around the circuit in the opposite direction reverses the sign of every term in the equation, which is like multiplying both sides of the equation by 

Figure 21.24 and the following points will help you get the plus or minus signs right when applying the loop rule. Note that the resistors and emfs are traversed by going from a to b. In many circuits, it will be necessary to construct more than one loop. In traversing each loop, one needs to be consistent for the sign of the change in potential. (See Example 21.5.)

  
FIGURE 21.24 Each of these resistors and voltage sources is traversed from a to b. The potential changes are shown beneath each element and are explained in the text. (Note that the script E stands for emf.)

• When a resistor is traversed in the same direction as the current, the change in potential is  . (See Figure 21.24.) When a resistor is traversed in the direction opposite to the current, the change in potential is  . (See Figure 21.24.) When an emf is traversed from to  (the same direction it moves positive charge), the change in potential is +emf. (See Figure 21.24.) When an emf is traversed from  to (opposite to the direction it moves positive charge), the change in potential is emf. (See Figure 21.24.)

# EXAMPLE 21.5

# Calculating Current: Using Kirchhoff’s Rules

Find the currents flowing in the circuit in Figure 21.25.  
FIGURE 21.25 This circuit is similar to that in Figure 21.21, but the resistances and emfs are specified. (Each emf is denoted by script E.) The currents in each branch are labeled and assumed to move in the directions shown. This example uses Kirchhoff’s rules to find the currents.

# Strategy

This circuit is sufficiently complex that the currents cannot be found using Ohm’s law and the series-parallel techniques—it is necessary to use Kirchhoff’s rules. Currents have been labeled  , and  in the figure and assumptions have been made about their directions. Locations on the diagram have been labeled with letters a through h. In the solution we will apply the junction and loop rules, seeking three independent equations to allow us to solve for the three unknown currents.

# Solution

We begin by applying Kirchhoff’s first or junction rule at point a. This gives



since  flows into the junction, while  and  flow out. Applying the junction rule at e produces exactly the same equation, so that no new information is obtained. This is a single equation with three unknowns—three independent equations are needed, and so the loop rule must be applied.

Now we consider the loop abcdea. Going from a to b, we traverse  in the same (assumed) direction of the current  , and so the change in potential is  . Then going from b to c, we go from to  , so that the change in potential is  . Traversing the internal resistance  from c to d gives  . Completing the loop by going from d to a again traverses a resistor in the same direction as its current, giving a change in potential of  .

The loop rule states that the changes in potential sum to zero. Thus,



Substituting values from the circuit diagram for the resistances and emf, and canceling the ampere unit gives



ow applying the loop rule to aefgha (we could have chosen abcdefgha as well) similarly gives



Note that the signs are reversed compared with the other loop, because elements are traversed in the opposite direction. With values entered, this becomes



These three equations are sufficient to solve for the three unknown currents. First, solve the second equation for 

Now solve the third equation for  :



Substituting these two new equations into the first one allows us to find a value for  :



Combining terms gives



Substituting this value for  back into the fourth equation gives



The minus sign means  flows in the direction opposite to that assumed in Figure 21.25.

Finally, substituting the value for  into the fifth equation gives





# Discussion

Just as a check, we note that indeed  . The results could also have been checked by entering all of the values into the equation for the abcdefgha loop.

# Problem-Solving Strategies for Kirchhoff’s Rules

1. Make certain there is a clear circuit diagram on which you can label all known and unknown resistances, emfs, and currents. If a current is unknown, you must assign it a direction. This is necessary for determining the signs of potential changes. If you assign the direction incorrectly, the current will be found to have a negative value—no harm done.   
2. Apply the junction rule to any junction in the circuit. Each time the junction rule is applied, you should get an equation with a current that does not appear in a previous application—if not, then the equation is redundant.   
3. Apply the loop rule to as many loops as needed to solve for the unknowns in the problem. (There must be as many independent equations as unknowns.) To apply the loop rule, you must choose a direction to go around the loop. Then carefully and consistently determine the signs of the potential changes for each element using the four bulleted points discussed above in conjunction with Figure 21.24.   
4. Solve the simultaneous equations for the unknowns. This may involve many algebraic steps, requiring careful checking and rechecking.   
5. Check to see whether the answers are reasonable and consistent. The numbers should be of the correct order of magnitude, neither exceedingly large nor vanishingly small. The signs should be reasonable—for example, no resistance should be negative. Check to see that the values obtained satisfy the various equations obtained from applying the rules. The currents should satisfy the junction rule, for example.

The material in this section is correct in theory. We should be able to verify it by making measurements of current and voltage. In fact, some of the devices used to make such measurements are straightforward applications of the principles covered so far and are explored in the next modules. As we shall see, a very basic, even profound, fact results—making a measurement alters the quantity being measured.# CHECK YOUR UNDERSTANDING

Can Kirchhoff’s rules be applied to simple series and parallel circuits or are they restricted for use in more complicated circuits that are not combinations of series and parallel?

# Solution

Kirchhoff's rules can be applied to any circuit since they are applications to circuits of two conservation laws. Conservation laws are the most broadly applicable principles in physics. It is usually mathematically simpler to use the rules for series and parallel in simpler circuits so we emphasize Kirchhoff’s rules for use in more complicated situations. But the rules for series and parallel can be derived from Kirchhoff’s rules. Moreover, Kirchhoff’s rules can be expanded to devices other than resistors and emfs, such as capacitors, and are one of the basic analysis devices in circuit analysis.

# 21.4 DC Voltmeters and Ammeters

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Explain why a voltmeter must be connected in parallel with the circuit.   
Draw a diagram showing an ammeter correctly connected in a circuit.   
Describe how a galvanometer can be used as either a voltmeter or an ammeter.   
Find the resistance that must be placed in series with a galvanometer to allow it to be used as a voltmeter with a given reading.   
Explain why measuring the voltage or current in a circuit can never be exact.

Voltmeters measure voltage, whereas ammeters measure current. Some of the meters in automobile dashboards, digital cameras, cell phones, and tuner-amplifiers are voltmeters or ammeters. (See Figure 21.26.) The internal construction of the simplest of these meters and how they are connected to the system they monitor give further insight into applications of series and parallel connections.

  
FIGURE 21.26 The fuel and temperature gauges (far right and far left, respectively) in this 1996 Volkswagen are voltmeters that register the voltage output of “sender” units, which are hopefully proportional to the amount of gasoline in the tank and the engine temperature. (credit: Christian Giersing)

Voltmeters are connected in parallel with whatever device’s voltage is to be measured. A parallel connection is used because objects in parallel experience the same potential difference. (See Figure 21.27, where the voltmeter is represented by the symbol V.)

Ammeters are connected in series with whatever device’s current is to be measured. A series connection is used because objects in series have the same current passing through them. (See Figure 21.28, where the ammeter is represented by the symbol A.)  
FIGURE 21.27 (a) To measure potential differences in this series circuit, the voltmeter  is placed in parallel with the voltage source or either of the resistors. Note that terminal voltage is measured between points a and b. It is not possible to connect the voltmeter directly across the emf without including its internal resistance,  . (b) A digital voltmeter in use. (credit: Messtechniker, Wikimedia Commons)

  
FIGURE 21.28 An ammeter (A) is placed in series to measure current. All of the current in this circuit flows through the meter. The ammeter would have the same reading if located between points d and e or between points f and a as it does in the position shown. (Note that the script capital E stands for emf, and  stands for the internal resistance of the source of potential difference.)

# Analog Meters: Galvanometers

Analog meters have a needle that swivels to point at numbers on a scale, as opposed to digital meters, which have numerical readouts similar to a hand-held calculator. The heart of most analog meters is a device called a galvanometer, denoted by G. Current flow through a galvanometer,  , produces a proportional needle deflection. (This deflection is due to the force of a magnetic field upon a current-carrying wire.)

The two crucial characteristics of a given galvanometer are its resistance and current sensitivity. Current sensitivity is the current that gives a full-scale deflection of the galvanometer’s needle, the maximum current that the instrument can measure. For example, a galvanometer with a current sensitivity of  has a maximum deflection of its needle when  flows through it, reads half-scale when  flows through it, and so on.If such a galvanometer has a  resistance, then a voltage of only  produces a full-scale reading. By connecting resistors to this galvanometer in different ways, you can use it as either a voltmeter or ammeter that can measure a broad range of voltages or currents.

# Galvanometer as Voltmeter

Figure 21.29 shows how a galvanometer can be used as a voltmeter by connecting it in series with a large resistance,  . The value of the resistance  is determined by the maximum voltage to be measured. Suppose you want  to produce a full-scale deflection of a voltmeter containing a  galvanometer with a  sensitivity. Then  applied to the meter must produce a current of  . The total resistance must be





(  is so large that the galvanometer resistance,  , is nearly negligible.) Note that  applied to this voltmeter produces a half-scale deflection by producing a  current through the meter, and so the voltmeter’s reading is proportional to voltage as desired.

This voltmeter would not be useful for voltages less than about half a volt, because the meter deflection would be small and difficult to read accurately. For other voltage ranges, other resistances are placed in series with the galvanometer. Many meters have a choice of scales. That choice involves switching an appropriate resistance into series with the galvanometer.



FIGURE 21.29 A large resistance  placed in series with a galvanometer G produces a voltmeter, the full-scale deflection of which depends on the choice of  . The larger the voltage to be measured, the larger  must be. (Note that  represents the internal resistance of the galvanometer.)

# Galvanometer as Ammeter

The same galvanometer can also be made into an ammeter by placing it in parallel with a small resistance  , often called the shunt resistance, as shown in Figure 21.30. Since the shunt resistance is small, most of the current passes through it, allowing an ammeter to measure currents much greater than those producing a full-scale deflection of the galvanometer.

Suppose, for example, an ammeter is needed that gives a full-scale deflection for  , and contains the same  galvanometer with its  sensitivity. Since  and  are in parallel, the voltage across them is the same.

These  drops are  so that . Solving for , and noting that is and is 0.999950 A, we have



  
FIGURE 21.30 A small shunt resistance  placed in parallel with a galvanometer G produces an ammeter, the full-scale deflection of which depends on the choice of  . The larger the current to be measured, the smaller  must be. Most of the current  flowing through the meter is shunted through  to protect the galvanometer. (Note that  represents the internal resistance of the galvanometer.) Ammeters may also have multiple scales for greater flexibility in application. The various scales are achieved by switching various shunt resistances in parallel with the galvanometer—the greater the maximum current to be measured, the smaller the shunt resistance must be.

# Taking Measurements Alters the Circuit

When you use a voltmeter or ammeter, you are connecting another resistor to an existing circuit and, thus, alteringthe circuit. Ideally, voltmeters and ammeters do not appreciably affect the circuit, but it is instructive to examine the circumstances under which they do or do not interfere.

First, consider the voltmeter, which is always placed in parallel with the device being measured. Very little current flows through the voltmeter if its resistance is a few orders of magnitude greater than the device, and so the circuit is not appreciably affected. (See Figure 21.31(a).) (A large resistance in parallel with a small one has a combined resistance essentially equal to the small one.) If, however, the voltmeter’s resistance is comparable to that of the device being measured, then the two in parallel have a smaller resistance, appreciably affecting the circuit. (See Figure 21.31(b).) The voltage across the device is not the same as when the voltmeter is out of the circuit.

  
FIGURE 21.31 (a) A voltmeter having a resistance much larger than the device  ) with which it is in parallel produces a parallel resistance essentially the same as the device and does not appreciably affect the circuit being measured. (b) Here the voltmeter has the same resistance as the device  , so that the parallel resistance is half of what it is when the voltmeter is not connected. This is an example of a significant alteration of the circuit and is to be avoided.

An ammeter is placed in series in the branch of the circuit being measured, so that its resistance adds to that branch. Normally, the ammeter’s resistance is very small compared with the resistances of the devices in the circuit, and so the extra resistance is negligible. (See Figure 21.32(a).) However, if very small load resistances are involved, or if the ammeter is not as low in resistance as it should be, then the total series resistance is significantly greater, and the current in the branch being measured is reduced. (See Figure 21.32(b).)

A practical problem can occur if the ammeter is connected incorrectly. If it was put in parallel with the resistor to measure the current in it, you could possibly damage the meter; the low resistance of the ammeter would allow most of the current in the circuit to go through the galvanometer, and this current would be larger since the effective resistance is smaller.

  
FIGURE 21.32 (a) An ammeter normally has such a small resistance that the total series resistance in the branch being measured is not appreciably increased. The circuit is essentially unaltered compared with when the ammeter is absent. (b) Here the ammeter’s resistance is the same as that of the branch, so that the total resistance is doubled and the current is half what it is without the ammeter. This significant alteration of the circuit is to be avoided.

One solution to the problem of voltmeters and ammeters interfering with the circuits being measured is to use galvanometers with greater sensitivity. This allows construction of voltmeters with greater resistance and ammeters with smaller resistance than when less sensitive galvanometers are used.

There are practical limits to galvanometer sensitivity, but it is possible to get analog meters that make measurements accurate to a few percent. Note that the inaccuracy comes from altering the circuit, not from a fault in the meter.

# Connections: Limits to Knowledge

Making a measurement alters the system being measured in a manner that produces uncertainty in themeasurement. For macroscopic systems, such as the circuits discussed in this module, the alteration can usually be made negligibly small, but it cannot be eliminated entirely. For submicroscopic systems, such as atoms, nuclei, and smaller particles, measurement alters the system in a manner that cannot be made arbitrarily small. This actually limits knowledge of the system—even limiting what nature can know about itself. We shall see profound implications of this when the Heisenberg uncertainty principle is discussed in the modules on quantum mechanics.

There is another measurement technique based on drawing no current at all and, hence, not altering the circuit at all. These are called null measurements and are the topic of Null Measurements. Digital meters that employ solid-state electronics and null measurements can attain accuracies of one part in  .

# CHECK YOUR UNDERSTANDING

Digital meters are able to detect smaller currents than analog meters employing galvanometers. How does this explain their ability to measure voltage and current more accurately than analog meters?

# Solution

Since digital meters require less current than analog meters, they alter the circuit less than analog meters. Their resistance as a voltmeter can be far greater than an analog meter, and their resistance as an ammeter can be far less than an analog meter. Consult Figure 21.27 and Figure 21.28 and their discussion in the text.

# PHET EXPLORATIONS

# Circuit Construction Kit (DC Only), Virtual Lab

Stimulate a neuron and monitor what happens. Pause, rewind, and move forward in time in order to observe the ions as they move across the neuron membrane.

Click to view content (https://openstax.org/books/college-physics-2e/pages/21-4-dc-voltmeters-and-ammeters)

# 21.5 Null Measurements

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Explain why a null measurement device is more accurate than a standard voltmeter or ammeter.   
Demonstrate how a Wheatstone bridge can be used to accurately calculate the resistance in a circuit.

Standard measurements of voltage and current alter the circuit being measured, introducing uncertainties in the measurements. Voltmeters draw some extra current, whereas ammeters reduce current flow. Null measurements balance voltages so that there is no current flowing through the measuring device and, therefore, no alteration of the circuit being measured.

Null measurements are generally more accurate but are also more complex than the use of standard voltmeters and ammeters, and they still have limits to their precision. In this module, we shall consider a few specific types of null measurements, because they are common and interesting, and they further illuminate principles of electric circuits.

# The Potentiometer

Suppose you wish to measure the emf of a battery. Consider what happens if you connect the battery directly to a standard voltmeter as shown in Figure 21.33. (Once we note the problems with this measurement, we will examine a null measurement that improves accuracy.) As discussed before, the actual quantity measured is the terminal voltage  , which is related to the emf of the battery by  , where  is the current that flows and  is the internal resistance of the battery.

The emf could be accurately calculated if  were very accurately known, but it is usually not. If the current  could be made zero, then  , and so emf could be directly measured. However, standard voltmeters need a current to operate; thus, another technique is needed.  
FIGURE 21.33 An analog voltmeter attached to a battery draws a small but nonzero current and measures a terminal voltage that differs from the emf of the battery. (Note that the script capital E symbolizes electromotive force, or emf.) Since the internal resistance of the battery is not known precisely, it is not possible to calculate the emf precisely.

A potentiometer is a null measurement device for measuring potentials (voltages). (See Figure 21.34.) A voltage source is connected to a resistor say, a long wire, and passes a constant current through it. There is a steady drop in potential (an  drop) along the wire, so that a variable potential can be obtained by making contact at varying locations along the wire.

Figure 21.34(b) shows an unknown  (represented by script  in the figure) connected in series with a galvanometer. Note that  opposes the other voltage source. The location of the contact point (see the arrow on the drawing) is adjusted until the galvanometer reads zero. When the galvanometer reads zero,  , where  is the resistance of the section of wire up to the contact point. Since no current flows through the galvanometer, none flows through the unknown emf, and so  is directly sensed.

Now, a very precisely known standard is substituted for  , and the contact point is adjusted until the galvanometer again reads zero, so that  . In both cases, no current passes through the galvanometer, and so the current  through the long wire is the same. Upon taking the ratio  ,  cancels, giving



Solving for  gives



  
FIGURE 21.34 The potentiometer, a null measurement device. (a) A voltage source connected to a long wire resistor passes a constant current  through it. (b) An unknown emf (labeled script  in the figure) is connected as shown, and the point of contact along  is adjusted until the galvanometer reads zero. The segment of wire has a resistance  and script  , where  is unaffected by the connection since no current flows through the galvanometer. The unknown emf is thus proportional to the resistance of the wire segment.

Because a long uniform wire is used for  , the ratio of resistances  is the same as the ratio of the lengths ofwire that zero the galvanometer for each emf. The three quantities on the right-hand side of the equation are now known or measured, and  can be calculated. The uncertainty in this calculation can be considerably smaller than when using a voltmeter directly, but it is not zero. There is always some uncertainty in the ratio of resistances  and in the standard . Furthermore, it is not possible to tell when the galvanometer reads exactly zero, which introduces error into both  and  , and may also affect the current  .

# Resistance Measurements and the Wheatstone Bridge

There is a variety of so-called ohmmeters that purport to measure resistance. What the most common ohmmeters actually do is to apply a voltage to a resistance, measure the current, and calculate the resistance using Ohm’s law. Their readout is this calculated resistance. Two configurations for ohmmeters using standard voltmeters and ammeters are shown in Figure 21.35. Such configurations are limited in accuracy, because the meters alter both the voltage applied to the resistor and the current that flows through it.

  
FIGURE 21.35 Two methods for measuring resistance with standard meters. (a) Assuming a known voltage for the source, an ammeter measures current, and resistance is calculated as  . (b) Since the terminal voltage  varies with current, it is better to measure it. is most accurately known when  is small, but  itself is most accurately known when it is large.

The Wheatstone bridge is a null measurement device for calculating resistance by balancing potential drops in a circuit. (See Figure 21.36.) The device is called a bridge because the galvanometer forms a bridge between two branches. A variety of bridge devices are used to make null measurements in circuits.

Resistors  and  are precisely known, while the arrow through  indicates that it is a variable resistance. The value of  can be precisely read. With the unknown resistance  in the circuit,  is adjusted until the galvanometer reads zero. The potential difference between points b and d is then zero, meaning that b and d are at the same potential. With no current running through the galvanometer, it has no effect on the rest of the circuit. So the branches abc and adc are in parallel, and each branch has the full voltage of the source. That is, the  drops along abc and adc are the same. Since b and d are at the same potential, the  drop along ad must equal the  drop along ab. Thus,



Again, since b and d are at the same potential, the  drop along dc must equal the  drop along bc. Thus,



Taking the ratio of these last two expressions gives



Canceling the currents and solving for  yields

  
FIGURE 21.36 The Wheatstone bridge is used to calculate unknown resistances. The variable resistance  is adjusted until the galvanometer reads zero with the switch closed. This simplifies the circuit, allowing  to be calculated based on the  drops as discussed in the text.

This equation is used to calculate the unknown resistance when current through the galvanometer is zero. This method can be very accurate (often to four significant digits), but it is limited by two factors. First, it is not possible to get the current through the galvanometer to be exactly zero. Second, there are always uncertainties in  , and  , which contribute to the uncertainty in  .

# CHECK YOUR UNDERSTANDING

Identify other factors that might limit the accuracy of null measurements. Would the use of a digital device that is more sensitive than a galvanometer improve the accuracy of null measurements?

# Solution

One factor would be resistance in the wires and connections in a null measurement. These are impossible to make zero, and they can change over time. Another factor would be temperature variations in resistance, which can be reduced but not completely eliminated by choice of material. Digital devices sensitive to smaller currents than analog devices do improve the accuracy of null measurements because they allow you to get the current closer to zero.

# 21.6 DC Circuits Containing Resistors and Capacitors

Explain the importance of the time constant, τ , and calculate the time constant for a given resistance and capacitance.   
Explain why batteries in a flashlight gradually lose power and the light dims over time.   
Describe what happens to a graph of the voltage across a capacitor over time as it charges.   
Explain how a timing circuit works and list some applications.   
Calculate the necessary speed of a strobe flash needed to “stop” the movement of an object over a particular length.

When you use a flash camera, it takes a few seconds to charge the capacitor that powers the flash. The light flash discharges the capacitor in a tiny fraction of a second. Why does charging take longer than discharging? This question and a number of other phenomena that involve charging and discharging capacitors are discussed in this module.

# RC Circuits

An RC circuit is one containing a resistor  and a capacitor C. The capacitor is an electrical component that stores electric charge.

Figure 21.37 shows a simple RC circuit that employs a DC (direct current) voltage source. The capacitor is initially uncharged. As soon as the switch is closed, current flows to and from the initially uncharged capacitor. As charge increases on the capacitor plates, there is increasing opposition to the flow of charge by the repulsion of like charges on each plate.In terms of voltage, this is because voltage across the capacitor is given by  , where  is the amount of charge stored on each plate and  is the capacitance. This voltage opposes the battery, growing from zero to the maximum emf when fully charged. The current thus decreases from its initial value of  to zero as the voltage on the capacitor reaches the same value as the emf. When there is no current, there is no  drop, and so the voltage on the capacitor must then equal the emf of the voltage source. This can also be explained with Kirchhoff’s second rule (the loop rule), discussed in Kirchhoff’s Rules, which says that the algebraic sum of changes in potential around any closed loop must be zero.

The initial current is  , because all of the  drop is in the resistance. Therefore, the smaller the resistance, the faster a given capacitor will be charged. Note that the internal resistance of the voltage source is included in  , as are the resistances of the capacitor and the connecting wires. In the flash camera scenario above, when the batteries powering the camera begin to wear out, their internal resistance rises, reducing the current and lengthening the time it takes to get ready for the next flash.

  
FIGURE 21.37 (a) An  circuit with an initially uncharged capacitor. Current flows in the direction shown (opposite of electron flow) as soon as the switch is closed. Mutual repulsion of like charges in the capacitor progressively slows the flow as the capacitor is charged, stopping the current when the capacitor is fully charged and  . (b) A graph of voltage across the capacitor versus time, with the switch closing at time  . (Note that in the two parts of the figure, the capital script E stands for emf,  stands for the charge stored on the capacitor, and  is the  time constant.)

Voltage on the capacitor is initially zero and rises rapidly at first, since the initial current is a maximum. Figure 21.37(b) shows a graph of capacitor voltage versus time  starting when the switch is closed at  . The voltage approaches emf asymptotically, since the closer it gets to emf the less current flows. The equation for voltage versus time when charging a capacitor  through a resistor  , derived using calculus, is



where  is the voltage across the capacitor, emf is equal to the emf of the DC voltage source, and the exponential e  is the base of the natural logarithm. Note that the units of  are seconds. We define



where  (the Greek letter tau) is called the time constant for an  circuit. As noted before, a small resistance  allows the capacitor to charge faster. This is reasonable, since a larger current flows through a smaller resistance. It is also reasonable that the smaller the capacitor  , the less time needed to charge it. Both factors are contained in  .

More quantitatively, consider what happens when  . Then the voltage on the capacitor is



This means that in the time  , the voltage rises to 0.632 of its final value. The voltage will rise 0.632 of the remainder in the next time  . It is a characteristic of the exponential function that the final value is never reached, but 0.632 of the remainder to that value is achieved in every time,  . In just a few multiples of the time constant  , then, the final value is very nearly achieved, as the graph in Figure 21.37(b) illustrates.

# Discharging a Capacitor

Discharging a capacitor through a resistor proceeds in a similar fashion, as Figure 21.38 illustrates. Initially, the current is  , driven by the initial voltage  on the capacitor. As the voltage decreases, the current andhence the rate of discharge decreases, implying another exponential formula for  . Using calculus, the voltage  on a capacitor  being discharged through a resistor  is found to be



  
FIGURE 21.38 (a) Closing the switch discharges the capacitor  through the resistor  . Mutual repulsion of like charges on each plate drives the current. (b) A graph of voltage across the capacitor versus time, with  at  . The voltage decreases exponentially, falling a fixed fraction of the way to zero in each subsequent time constant  .

The graph in Figure 21.38(b) is an example of this exponential decay. Again, the time constant is  . A small resistance  allows the capacitor to discharge in a small time, since the current is larger. Similarly, a small capacitance requires less time to discharge, since less charge is stored. In the first time interval  after the switch is closed, the voltage falls to 0.368 of its initial value, since  .

During each successive time  , the voltage falls to 0.368 of its preceding value. In a few multiples of  , the voltage becomes very close to zero, as indicated by the graph in Figure 21.38(b).

Now we can explain why the flash camera in our scenario takes so much longer to charge than discharge; the resistance while charging is significantly greater than while discharging. The internal resistance of the battery accounts for most of the resistance while charging. As the battery ages, the increasing internal resistance makes the charging process even slower. (You may have noticed this.)

The flash discharge is through a low-resistance ionized gas in the flash tube and proceeds very rapidly. Flash photographs, such as in Figure 21.39, can capture a brief instant of a rapid motion because the flash can be less than a microsecond in duration. Such flashes can be made extremely intense.

During World War II, nighttime reconnaissance photographs were made from the air with a single flash illuminating more than a square kilometer of enemy territory. The brevity of the flash eliminated blurring due to the surveillance aircraft’s motion. Today, an important use of intense flash lamps is to pump energy into a laser. The short intense flash can rapidly energize a laser and allow it to reemit the energy in another form.

  
FIGURE 21.39 This stop-motion photograph of a rufous hummingbird (Selasphorus rufus) feeding on a flower was obtained with an extremely brief and intense flash of light powered by the discharge of a capacitor through a gas. (credit: Dean E. Biggins, U.S. Fish and Wildlife Service)# EXAMPLE 21.6

# Integrated Concept Problem: Calculating Capacitor Size—Strobe Lights

High-speed flash photography was pioneered by Doc Edgerton in the 1930s, while he was a professor of electrical engineering at MIT. You might have seen examples of his work in the amazing shots of hummingbirds in motion, a drop of milk splattering on a table, or a bullet penetrating an apple (see Figure 21.39). To stop the motion and capture these pictures, one needs a high-intensity, very short pulsed flash, as mentioned earlier in this module.

Suppose one wished to capture the picture of a bullet (moving at  that was passing through an apple. The duration of the flash is related to the  time constant,  . What size capacitor would one need in the  circuit to succeed, if the resistance of the flash tube was  Assume the apple is a sphere with a diameter of 

# Strategy

We begin by identifying the physical principles involved. This example deals with the strobe light, as discussed above. Figure 21.38 shows the circuit for this probe. The characteristic time  of the strobe is given as 

# Solution

We wish to find  , but we don’t know  . We want the flash to be on only while the bullet traverses the apple. So we need to use the kinematic equations that describe the relationship between distance  , velocity  , and time  :



The bullet’s velocity is given as  , and the distance  is  The traverse time, then, is



We set this value for the crossing time  equal to  . Therefore,



(Note: Capacitance  is typically measured in farads,  , defined as Coulombs per volt. From the equation, we see that  can also be stated in units of seconds per ohm.)

# Discussion

The flash interval of  (the traverse time of the bullet) is relatively easy to obtain today. Strobe lights have opened up new worlds from science to entertainment. The information from the picture of the apple and bullet was used in the Warren Commission Report on the assassination of President John F. Kennedy in 1963 to confirm that only one bullet was fired.

# RC Circuits for Timing

 circuits are commonly used for timing purposes. A mundane example of this is found in the ubiquitous intermittent wiper systems of modern cars. The time between wipes is varied by adjusting the resistance in an circuit. Another example of an  circuit is found in novelty jewelry, Halloween costumes, and various toys that have battery-powered flashing lights. (See Figure 21.40 for a timing circuit.)

A more crucial use of  circuits for timing purposes is in the artificial pacemaker, used to control heart rate. The heart rate is normally controlled by electrical signals generated by the sino-atrial (SA) node, which is on the wall of the right atrium chamber. This causes the muscles to contract and pump blood. Sometimes the heart rhythm is abnormal and the heartbeat is too high or too low.

The artificial pacemaker is inserted near the heart to provide electrical signals to the heart when needed with theappropriate time constant. Pacemakers have sensors that detect body motion and breathing to increase the heart rate during exercise to meet the body’s increased needs for blood and oxygen.

  
FIGURE 21.40 (a) The lamp in this  circuit ordinarily has a very high resistance, so that the battery charges the capacitor as if the lamp were not there. When the voltage reaches a threshold value, a current flows through the lamp that dramatically reduces its resistance, and the capacitor discharges through the lamp as if the battery and charging resistor were not there. Once discharged, the process starts again, with the flash period determined by the  constant  . (b) A graph of voltage versus time for this circuit.

# EXAMPLE 21.7

# Calculating Time: RC Circuit in a Heart Defibrillator

A heart defibrillator is used to resuscitate an accident victim by discharging a capacitor through the trunk of her body. A simplified version of the circuit is seen in Figure 21.38. (a) What is the time constant if an  capacitor is used and the path resistance through her body is  (b) If the initial voltage is  , how long does it take to decline to  ?

# Strategy

Since the resistance and capacitance are given, it is straightforward to multiply them to give the time constant asked for in part (a). To find the time for the voltage to decline to  , we repeatedly multiply the initial voltage by 0.368 until a voltage less than or equal to  is obtained. Each multiplication corresponds to a time of  seconds.

# Solution for (a)

The time constant  is given by the equation  . Entering the given values for resistance and capacitance (and remembering that units for a farad can be expressed as  ) gives



# Solution for (b)

In the first  , the voltage  declines to 0.368 of its initial value. That is:



(Notice that we carry an extra digit for each intermediate calculation.) After another 8.00 ms, we multiply by 0.368 again, and the voltage is

Similarly, after another  , the voltage is



# Discussion

So after only  , the voltage is down to  , or  of its original value.Such brief times are useful in heart defibrillation, because the brief but intense current causes a brief but effective contraction of the heart. The actual circuit in a heart defibrillator is slightly more complex than the one in Figure 21.38, to compensate for magnetic and AC effects that will be covered in Magnetism.

# CHECK YOUR UNDERSTANDING

When is the potential difference across a capacitor an emf?

# Solution

Only when the current being drawn from or put into the capacitor is zero. Capacitors, like batteries, have internal resistance, so their output voltage is not an emf unless current is zero. This is difficult to measure in practice so we refer to a capacitor’s voltage rather than its emf. But the source of potential difference in a capacitor is fundamental and it is an emf.

# PHET EXPLORATIONS

# Circuit Construction Kit (DC only)

An electronics kit in your computer! Build circuits with resistors, light bulbs, batteries, and switches. Take measurements with the realistic ammeter and voltmeter. View the circuit as a schematic diagram, or switch to a lifelike view.

Click to view content (https://openstax.org/books/college-physics-2e/pages/21-6-dc-circuits-containing-resistorsand-capacitors)# Glossary

ammeter an instrument that measures current   
analog meter a measuring instrument that gives a readout in the form of a needle movement over a marked gauge   
bridge device a device that forms a bridge between two branches of a circuit; some bridge devices are used to make null measurements in circuits   
capacitance the maximum amount of electric potential energy that can be stored (or separated) for a given electric potential   
capacitor an electrical component used to store energy by separating electric charge on two opposing plates   
conservation laws require that energy and charge be conserved in a system   
current the flow of charge through an electric circuit past a given point of measurement   
current sensitivity the maximum current that a galvanometer can read   
digital meter a measuring instrument that gives a readout in a digital form   
electromotive force (emf) the potential difference of a source of electricity when no current is flowing; measured in volts   
full-scale deflection the maximum deflection of a galvanometer needle, also known as current sensitivity; a galvanometer with a full-scale deflection of  has a maximum deflection of its needle when  flows through it   
galvanometer an analog measuring device, denoted by G, that measures current flow using a needle deflection caused by a magnetic field force acting upon a current-carrying wire   
internal resistance the amount of resistance within the voltage source   
Joule’s law the relationship between potential electrical power, voltage, and resistance in an electrical circuit, given by:    
junction rule Kirchhoff’s first rule, which applies the conservation of charge to a junction; current is the flow of charge; thus, whatever charge flows into the junction must flow out; the rule can be stated    
Kirchhoff’s rules a set of two rules, based on conservation of charge and energy, governing current and changes in potential in an electric circuit   
loop rule Kirchhoff’s second rule, which states that in a closed loop, whatever energy is supplied by emf must be transferred into other forms by devices in the loop, since there are no other ways in which energy can be transferred into or out of the circuit. Thus, the emf equals the sum of the  (voltage) drops in the loop and can be stated:    
null measurements methods of measuring current and voltage more accurately by balancing the circuit so that no current flows through the measurement device   
Ohm’s law the relationship between current, voltage, and resistance within an electrical circuit:    
ohmmeter an instrument that applies a voltage to a resistance, measures the current, calculates the resistance using Ohm’s law, and provides a readout of this calculated resistance   
parallel the wiring of resistors or other components in an electrical circuit such that each component receives an equal voltage from the power source; often pictured in a ladder-shaped diagram, with each component on a rung of the ladder   
potential difference the difference in electric potential between two points in an electric circuit, measured in volts   
potentiometer a null measurement device for measuring potentials (voltages)   
RC circuit a circuit that contains both a resistor and a capacitor   
resistance causing a loss of electrical power in a circuit   
resistor a component that provides resistance to the current flowing through an electrical circuit   
series a sequence of resistors or other components wired into a circuit one after the other   
shunt resistance a small resistance  placed in parallel with a galvanometer G to produce an ammeter; the larger the current to be measured, the smaller  must be; most of the current flowing through the meter is shunted through  to protect the galvanometer   
terminal voltage the voltage measured across the terminals of a source of potential difference   
voltage the electrical potential energy per unit charge; electric pressure created by a power source, such as a battery   
voltage drop the loss of electrical power as a current travels through a resistor, wire or other component   
voltmeter an instrument that measures voltage   
Wheatstone bridge a null measurement device for calculating resistance by balancing potential drops in a circuit# Section Summary

# 21.1 Resistors in Series and Parallel

• The total resistance of an electrical circuit with resistors wired in a series is the sum of the individual resistances:  Each resistor in a series circuit has the same amount of current flowing through it. The voltage drop, or power dissipation, across each individual resistor in a series is different, and their combined total adds up to the power source input. The total resistance of an electrical circuit with resistors wired in parallel is less than the lowest resistance of any of the components and can be determined using the formula:  Each resistor in a parallel circuit has the same full voltage of the source applied to it. The current flowing through each resistor in a parallel circuit is different, depending on the resistance. If a more complex connection of resistors is a combination of series and parallel, it can be reduced to a single equivalent resistance by identifying its various parts as series or parallel, reducing each to its equivalent, and continuing until a single resistance is eventually reached.

# 21.2 Electromotive Force: Terminal Voltage

• All voltage sources have two fundamental parts—a source of electrical energy that has a characteristic electromotive force (emf), and an internal resistance  . The emf is the potential difference of a source when no current is flowing.   
• The numerical value of the emf depends on the source of potential difference.   
• The internal resistance  of a voltage source affects the output voltage when a current flows.   
The voltage output of a device is called its terminal voltage  and is given by  , where  is the electric current and is positive when flowing away from the positive terminal of the voltage source. When multiple voltage sources are in series, their internal resistances add and their emfs add algebraically. Solar cells can be wired in series or parallel to provide increased voltage or current, respectively.

# 21.3 Kirchhoff’s Rules

• Kirchhoff’s rules can be used to analyze any circuit, simple or complex. Kirchhoff’s first rule—the junction rule: The sum of all currents entering a junction must equal the sum of all currents leaving the junction. Kirchhoff’s second rule—the loop rule: The algebraic sum of changes in potential around any closed circuit path (loop) must be zero. The two rules are based, respectively, on the laws of conservation of charge and energy. When calculating potential and current using Kirchhoff’s rules, a set of conventions must be followed for determining the correct signs of various terms. The simpler series and parallel rules are special cases of Kirchhoff’s rules.

# 21.4 DC Voltmeters and Ammeters

• Voltmeters measure voltage, and ammeters measure current. A voltmeter is placed in parallel with the voltage source to receive full voltage and must have a large resistance to limit its effect on the circuit. An ammeter is placed in series to get the full current flowing through a branch and must have a small resistance to limit its effect on the circuit. Both can be based on the combination of a resistor and a galvanometer, a device that gives an analog reading of current. Standard voltmeters and ammeters alter the circuit being measured and are thus limited in accuracy.

# 21.5 Null Measurements

• Null measurement techniques achieve greater accuracy by balancing a circuit so that no current flows through the measuring device. One such device, for determining voltage, is a potentiometer. Another null measurement device, for determining resistance, is the Wheatstone bridge. Other physical quantities can also be measured with null measurement techniques.

# 21.6 DC Circuits Containing Resistors and Capacitors

• An  circuit is one that has both a resistor and a capacitor. • The time constant  for an  circuit is  . • When an initially uncharged  at  )capacitor in series with a resistor is charged by a DC voltage source, the voltage rises, asymptotically approaching the emf of the voltage source; as a function of time,  (charging). Within the span of each time constant  , the voltage rises by 0.632 of the remaining value, approaching the final voltage asymptotically.

• If a capacitor with an initial voltage  is discharged through a resistor starting at  , then its voltage decreases exponentially as given by  (discharging). In each time constant  , the voltage falls by 0.368 of its remaining initial value, approaching zero asymptotically.

# Conceptual Questions

# 21.1 Resistors in Series and Parallel

1. A switch has a variable resistance that is nearly zero when closed and extremely large when open, and it is placed in series with the device it controls. Explain the effect the switch in Figure 21.41 has on current when open and when closed.

  
FIGURE 21.41 A switch is ordinarily in series with a resistance and voltage source. Ideally, the switch has nearly zero resistance when closed but has an extremely large resistance when open. (Note that in this diagram, the script E represents the voltage (or electromotive force) of the battery.)

2. What is the voltage across the open switch in Figure 21.41?

3. There is a voltage across an open switch, such as in Figure 21.41. Why, then, is the power dissipated by the open switch small?

4. Why is the power dissipated by a closed switch, such as in Figure 21.41, small?

5. A student in a physics lab mistakenly wired a light bulb, battery, and switch as shown in Figure 21.42. Explain why the bulb is on when the switch is open, and off when the switch is closed. (Do not try this—it is hard on the battery!)

  
FIGURE 21.42 A wiring mistake put this switch in parallel with the device represented by . (Note that in this diagram, the script E represents the voltage (or electromotive force) of the battery.)

6. Knowing that the severity of a shock depends on the magnitude of the current through your body, would you prefer to be in series or parallel with a resistance, such as the heating element of a toaster, if shocked by it? Explain.

7. Would your headlights dim when you start your car’s engine if the wires in your automobile were superconductors? (Do not neglect the battery’s internal resistance.) Explain.

8. Some strings of holiday lights are wired in series to save wiring costs. An old version utilized bulbs that break the electrical connection, like an open switch, when they burn out. If one such bulb burns out, what happens to the others? If such a string operates on  and has 40 identical bulbs, what is the normal operating voltage of each? Newer versions use bulbs that short circuit, like a closed switch, when they burn out. If one such bulb burns out, what happens to the others? If such a string operates on  and has 39 remaining identical bulbs, what is then the operating voltage of each?

9. If two household lightbulbs rated 60 W and 100 W are connected in series to household power, which will be brighter? Explain.10. Suppose you are doing a physics lab that asks you to put a resistor into a circuit, but all the resistors supplied have a larger resistance than the requested value. How would you connect the available resistances to attempt to get the smaller value asked for?

11. Before World War II, some radios got power through a “resistance cord” that had a significant resistance. Such a resistance cord reduces the voltage to a desired level for the radio’s tubes and the like, and it saves the expense of a transformer. Explain why resistance cords become warm and waste energy when the radio is on.

12. Some light bulbs have three power settings (not including zero), obtained from multiple filaments that are individually switched and wired in parallel. What is the minimum number of filaments needed for three power settings?

# 21.2 Electromotive Force: Terminal Voltage

13. Is every emf a potential difference? Is every potential difference an emf? Explain.

14. Explain which battery is doing the charging and which is being charged in Figure 21.43.

  
FIGURE 21.43

15. Given a battery, an assortment of resistors, and a variety of voltage and current measuring devices, describe how you would determine the internal resistance of the battery.

16. Two different  automobile batteries on a store shelf are rated at 600 and 850 “cold cranking amps.” Which has the smallest internal resistance?

17. What are the advantages and disadvantages of connecting batteries in series? In parallel?

18. Semitractor trucks use four large 12-V batteries. The starter system requires  , while normal operation of the truck’s other electrical components utilizes  . How could the four batteries be connected to produce 24 V? To produce 12 V? Why is  better than  for starting the truck’s engine (a very heavy load)?

# 21.3 Kirchhoff’s Rules

19. Can all of the currents going into the junction in Figure 21.44 be positive? Explain.

  
FIGURE 21.44

20. Apply the junction rule to junction b in Figure 21.45. Is any new information gained by applying the junction rule at e? (In the figure, each emf is represented by script E.)

  
FIGURE 21.45

21. (a) What is the potential difference going from point a to point b in Figure 21.45? (b) What is the potential difference going from c to b? (c) From e to  (d) From e to d?

22. Apply the loop rule to loop afedcba in Figure 21.45.

23. Apply the loop rule to loops abgefa and cbgedc in Figure 21.45.

# 21.4 DC Voltmeters and Ammeters

24. Why should you not connect an ammeter directly across a voltage source as shown in Figure 21.46? (Note that script E in the figure stands for emf.)

25. Suppose you are using a multimeter (one designed to measure a range of voltages, currents, and resistances) to measure current in a circuit and you inadvertently leave it in a voltmeter mode. What effect will the meter have on the circuit? What would happen if you were measuring voltage but accidentally put the meter in the ammeter mode?

26. Specify the points to which you could connect a voltmeter to measure the following potential differences in Figure 21.47: (a) the potential difference of the voltage source; (b) the potential difference across  ; (c) across  ; (d) across  ; (e) across  and  . Note that there may be more than one answer to each part.

  
FIGURE 21.47

27. To measure currents in Figure 21.47, you would replace a wire between two points with an ammeter. Specify the points between which you would place an ammeter to measure the following: (a) the total current; (b) the current flowing through  ; (c) through  ; (d) through  . Note that there may be more than one answer to each part.

# 21.5 Null Measurements

28. Why can a null measurement be more accurate than one using standard voltmeters and ammeters? What factors limit the accuracy of null measurements?

29. If a potentiometer is used to measure cell emfs on the order of a few volts, why is it most accurate for the standard  to be the same order of magnitude and the resistances to be in the range of a few ohms?

# 21.6 DC Circuits Containing Resistors and Capacitors

30. Regarding the units involved in the relationship  , verify that the units of resistance times capacitance are time, that is,  .

31. The  time constant in heart defibrillation is crucial to limiting the time the current flows. If the capacitance in the defibrillation unit is fixed, how would you manipulate resistance in the circuit to adjust the  constant  Would an adjustment of the applied voltage also be needed to ensure that the current delivered has an appropriate value?

32. When making an ECG measurement, it is important to measure voltage variations over small time intervals. The time is limited by the  constant of the circuit—it is not possible to measure time variations shorter than . How would you manipulate  and  in the circuit to allow the necessary measurements?

33. Draw two graphs of charge versus time on a capacitor. Draw one for charging an initially uncharged capacitor in series with a resistor, as in the circuit in Figure 21.37, starting from  . Draw the other for discharging a capacitor through a resistor, as in the circuit in Figure 21.38, starting at  , with an initial charge  . Show at least two intervals of  .

34. When charging a capacitor, as discussed in conjunction with Figure 21.37, how long does it take for the voltage on the capacitor to reach emf? Is this a problem?

35. When discharging a capacitor, as discussed in conjunction with Figure 21.38, how long does it take for the voltage on the capacitor to reach zero? Is this a problem?

36. Referring to Figure 21.37, draw a graph of potential difference across the resistor versus time, showing at least two intervals of . Also draw a graph of current versus time for this situation.

37. A long, inexpensive extension cord is connected from inside the house to a refrigerator outside. The refrigerator doesn’t run as it should. What might be the problem?

38. In Figure 21.40, does the graph indicate the time constant is shorter for discharging than for charging? Would you expect ionized gas to have low resistance? How would you adjust  to get a longer time between flashes? Would adjusting  affect the discharge time?39. An electronic apparatus may have large capacitors at high voltage in the power supply section, presenting a shock hazard even when the apparatus is switched off. A “bleeder resistor” is therefore placed across such a capacitor, as shown schematically in Figure 21.48, to bleed the charge from it after the apparatus is off. Why must the bleeder resistance be much greater than the effective resistance of the rest of the circuit? How does this affect the time constant for discharging the capacitor?

  
FIGURE 21.48 A bleeder resistor  discharges the capacitor in this electronic device once it is switched off.

# Problems & Exercises

# 21.1 Resistors in Series and Parallel

# Note: Data taken from figures can be assumed to be accurate to three significant digits.

1. (a) What is the resistance of ten resistors connected in series? (b) In parallel?   
2. (a) What is the resistance of a  , a  , and a  resistor connected in series? (b) In parallel?   
3. What are the largest and smallest resistances you can obtain by connecting a  , a , and a resistor together?   
4. An 1800-W toaster, a 1400-W electric frying pan, and a 75-W lamp are plugged into the same outlet in a 15-A, 120-V circuit. (The three devices are in parallel when plugged into the same socket.). (a) What current is drawn by each device? (b) Will this combination blow the 15-A fuse?   
5. Your car’s 30.0-W headlight and 2.40-kW starter are ordinarily connected in parallel in a 12.0-V system. What power would one headlight and the starter consume if connected in series to a  battery? (Neglect any other resistance in the circuit and any change in resistance in the two devices.)   
6. (a) Given a 48.0-V battery and  and  resistors, find the current and power for each when connected in series. (b) Repeat when the resistances are in parallel.   
7. Referring to the example combining series and parallel circuits and Figure  , calculate  in the following two different ways: (a) from the known values of  and  ; (b) using Ohm’s law for  . In both parts explicitly show how you follow the steps in the Problem-Solving Strategies for Series and Parallel Resistors.   
8. Referring to Figure 21.6: (a) Calculate  and note how it compares with  found in the first two example problems in this module. (b) Find the total power supplied by the source and compare it with the sum of the powers dissipated by the resistors.   
9. Refer to Figure 21.7 and the discussion of lights dimming when a heavy appliance comes on. (a) Given the voltage source is  , the wire resistance is  , and the bulb is nominally 75.0 W, what power will the bulb dissipate if a total of 15.0 A passes through the wires when the motor comes on? Assume negligible change in bulb resistance. (b) What power is consumed by the motor?10. A 240-kV power transmission line carrying  is hung from grounded metal towers by ceramic insulators, each having a  resistance. Figure 21.49. (a) What is the resistance to ground of 100 of these insulators? (b) Calculate the power dissipated by 100 of them. (c) What fraction of the power carried by the line is this? Explicitly show how you follow the steps in the Problem-Solving Strategies for Series and Parallel Resistors.

  
FIGURE 21.49 High-voltage (240-kV) transmission line carrying  is hung from a grounded metal transmission tower. The row of ceramic insulators provide  of resistance each.

11. Show that if two resistors  and  are combined and one is much greater than the other  : (a) Their series resistance is very nearly equal to the greater resistance  . (b) Their parallel resistance is very nearly equal to smaller resistance  .

12. Unreasonable Results Two resistors, one having a resistance of  , are connected in parallel to produce a total resistance of  . (a) What is the value of the second resistance? (b) What is unreasonable about this result? (c) Which assumptions are unreasonable or inconsistent?

13. Unreasonable Results Two resistors, one having a resistance of  are connected in series to produce a total resistance of  . (a) What is the value of the second resistance? (b) What is unreasonable about this result? (c) Which assumptions are unreasonable or inconsistent?

# 21.2 Electromotive Force: Terminal Voltage

14. Standard automobile batteries have six lead-acid cells in series, creating a total emf of 12.0 V. What is the emf of an individual lead-acid cell?

15. Carbon-zinc dry cells (sometimes referred to as non-alkaline cells) have an emf of  , and they are produced as single cells or in various combinations to form other voltages. (a) How many 1.54-V cells are needed to make the common 9-V battery used in many small electronic devices? (b) What is the actual emf of the approximately 9-V battery? (c) Discuss how internal resistance in the series connection of cells will affect the terminal voltage of this approximately 9-V battery.

16. What is the output voltage of a 3.0000-V lithium cell in a digital wristwatch that draws  , if the cell’s internal resistance is 

17. (a) What is the terminal voltage of a large 1.54-V carbon-zinc dry cell used in a physics lab to supply 2.00 A to a circuit, if the cell’s internal resistance is  (b) How much electrical power does the cell produce? (c) What power goes to its load?

18. What is the internal resistance of an automobile battery that has an emf of  and a terminal voltage of  while a current of 8.00 A is charging it?

19. (a) Find the terminal voltage of a  motorcycle battery having a  internal resistance, if it is being charged by a current of 10.0 A. (b) What is the output voltage of the battery charger?

20. A car battery with a 12-V emf and an internal resistance of  is being charged with a current of 60 A. Note that in this process the battery is being charged. (a) What is the potential difference across its terminals? (b) At what rate is thermal energy being dissipated in the battery? (c) At what rate is electric energy being converted to chemical energy? (d) What are the answers to (a) and (b) when the battery is used to supply 60 A to the starter motor?

21. The hot resistance of a flashlight bulb is  , and it is run by a 1.58-V alkaline cell having a  internal resistance. (a) What current flows? (b) Calculate the power supplied to the bulb using  . (c) Is this power the same as calculated using 22. The label on a portable radio recommends the use of rechargeable nickel-cadmium cells (nicads), although they have a 1.25-V emf while alkaline cells have a 1.58-V emf. The radio has a  resistance. (a) Draw a circuit diagram of the radio and its batteries. Now, calculate the power delivered to the radio. (b) When using Nicad cells each having an internal resistance of  . (c) When using alkaline cells each having an internal resistance of  . (d) Does this difference seem significant, considering that the radio’s effective resistance is lowered when its volume is turned up?

23. An automobile starter motor has an equivalent resistance of  and is supplied by a  battery with  internal resistance. (a) What is the current to the motor? (b) What voltage is applied to it? (c) What power is supplied to the motor? (d) Repeat these calculations for when the battery connections are corroded and add  to the circuit. (Significant problems are caused by even small amounts of unwanted resistance in low-voltage, high-current applications.)

24. A child’s electronic toy is supplied by three 1.58-V alkaline cells having internal resistances of  in series with a 1.53-V carbon-zinc dry cell having a internal resistance. The load resistance is  . (a) Draw a circuit diagram of the toy and its batteries. (b) What current flows? (c) How much power is supplied to the load? (d) What is the internal resistance of the dry cell if it goes bad, resulting in only 0.500 W being supplied to the load?

25. (a) What is the internal resistance of a voltage source if its terminal voltage drops by  when the current supplied increases by 5.00 A? (b) Can the emf of the voltage source be found with the information supplied?

26. A person with body resistance between his hands of  accidentally grasps the terminals of a  power supply. (Do NOT do this!) (a) Draw a circuit diagram to represent the situation. (b) If the internal resistance of the power supply is  , what is the current through his body? (c) What is the power dissipated in his body? (d) If the power supply is to be made safe by increasing its internal resistance, what should the internal resistance be for the maximum current in this situation to be  or less? (e) Will this modification compromise the effectiveness of the power supply for driving low-resistance devices? Explain your reasoning.

27. Electric fish generate current with biological cells called electroplaques, which are physiological emf devices. The electroplaques in the South American eel are arranged in 140 rows, each row stretching horizontally along the body and each containing 5000 electroplaques. Each electroplaque has an emf of  and internal resistance of  . If the water surrounding the fish has resistance of  , how much current can the eel produce in water from near its head to near its tail?

28. Integrated Concepts A 12.0-V emf automobile battery has a terminal voltage of  when being charged by a current of 10.0 A. (a) What is the battery’s internal resistance? (b) What power is dissipated inside the battery? (c) At what rate (in  ) will its temperature increase if its mass is  and it has a specific heat of  assuming no heat escapes?

29. Unreasonable Results A 1.58-V alkaline cell with a  internal resistance is supplying 8.50 A to a load. (a) What is its terminal voltage? (b) What is the value of the load resistance? (c) What is unreasonable about these results? (d) Which assumptions are unreasonable or inconsistent?

30. Unreasonable Results (a) What is the internal resistance of a 1.54-V dry cell that supplies 1.00 W of power to a bulb? (b) What is unreasonable about this result? (c) Which assumptions are unreasonable or inconsistent?

# 21.3 Kirchhoff’s Rules

31. Apply the loop rule to loop abcdefgha in Figure 21.25.   
32. Apply the loop rule to loop aedcba in Figure 21.25.   
33. Verify the second equation in Example 21.5 by substituting the values found for the currents  and  .   
34. Verify the third equation in Example 21.5 by substituting the values found for the currents  and  .35. Apply the junction rule at point a in Figure 21.50.

  
FIGURE 21.50

36. Apply the loop rule to loop abcdefghija in Figure 21.50.

37. Apply the loop rule to loop akledcba in Figure 21.50.

38. Find the currents flowing in the circuit in Figure 21.50. Explicitly show how you follow the steps in the Problem-Solving Strategies for Series and Parallel Resistors.

39. Solve Example 21.5, but use loop abcdefgha instead of loop akledcba. Explicitly show how you follow the steps in the Problem-Solving Strategies for Series and Parallel Resistors.

40. Find the currents flowing in the circuit in Figure 21.45.

41. Unreasonable Results Consider the circuit in Figure 21.51, and suppose that the emfs are unknown and the currents are given to be  ,  , and  . (a) Could you find the emfs? (b) What is wrong with the assumptions?

  
FIGURE 21.51

# 21.4 DC Voltmeters and Ammeters

42. What is the sensitivity of the galvanometer (that is, what current gives a full-scale deflection) inside a voltmeter that has a resistance on its 30.0-V scale?

43. What is the sensitivity of the galvanometer (that is, what current gives a full-scale deflection) inside a voltmeter that has a  resistance on its 100-V scale?

44. Find the resistance that must be placed in series with  galvanometer having a  sensitivity (the same as the one discussed in the text) to allow it to be used as a voltmeter with a 0.100-V full-scale reading.

45. Find the resistance that must be placed in series with a galvanometer having a  sensitivity (the same as the one discussed in the text) to allow it to be used as a voltmeter with a 3000-V full-scale reading. Include a circuit diagram with your solution.

46. Find the resistance that must be placed in parallel with a  galvanometer having a  sensitivity (the same as the one discussed in the text) to allow it to be used as an ammeter with a 10.0-A full-scale reading. Include a circuit diagram with your solution.

47. Find the resistance that must be placed in parallel with a  galvanometer having a  sensitivity (the same as the one discussed in the text) to allow it to be used as an ammeter with a  full-scale reading.

48. Find the resistance that must be placed in series with a  galvanometer having a  sensitivity to allow it to be used as a voltmeter with: (a) a 300-V full-scale reading, and (b) a 0.300-V full-scale reading.

49. Find the resistance that must be placed in parallel with a  galvanometer having a  sensitivity to allow it to be used as an ammeter with: (a) a 20.0-A full-scale reading, and (b) a  full-scale reading.50. Suppose you measure the terminal voltage of a 1.585-V alkaline cell having an internal resistance of  by placing a  voltmeter across its terminals. (See Figure 21.52.) (a) What current flows? (b) Find the terminal voltage. (c) To see how close the measured terminal voltage is to the emf, calculate their ratio.

  
FIGURE 21.52

51. Suppose you measure the terminal voltage of a 3.200-V lithium cell having an internal resistance of  by placing a  voltmeter across its terminals. (a) What current flows? (b) Find the terminal voltage. (c) To see how close the measured terminal voltage is to the emf, calculate their ratio.

52. A certain ammeter has a resistance of  on its 3.00-A scale and contains a  galvanometer. What is the sensitivity of the galvanometer?

53. A voltmeter is placed in parallel with a  resistor in a circuit. (a) Draw a circuit diagram of the connection. (b) What is the resistance of the combination? (c) If the voltage across the combination is kept the same as it was across the  resistor alone, what is the percent increase in current? (d) If the current through the combination is kept the same as it was through the  resistor alone, what is the percentage decrease in voltage? (e) Are the changes found in parts (c) and (d) significant? Discuss.

54. A ammeter is placed in series with a resistor in a circuit. (a) Draw a circuit diagram of the connection. (b) Calculate the resistance of the combination. (c) If the voltage is kept the same across the combination as it was through the resistor alone, what is the percent decrease in current? (d) If the current is kept the same through the combination as it was through the resistor alone, what is the percent increase in voltage? (e) Are the changes found in parts (c) and (d) significant? Discuss.

55. Unreasonable Results Suppose you have a  galvanometer with a  sensitivity. (a) What resistance would you put in series with it to allow it to be used as a voltmeter that has a full-scale deflection for 0.500 mV? (b) What is unreasonable about this result? (c) Which assumptions are responsible?

56. Unreasonable Results (a) What resistance would you put in parallel with a  galvanometer having a  sensitivity to allow it to be used as an ammeter that has a full-scale deflection for  (b) What is unreasonable about this result? (c) Which assumptions are responsible?

# 21.5 Null Measurements

57. What is the  of a cell being measured in a potentiometer, if the standard cell’s emf is  and the potentiometer balances for  and 

58. Calculate the  of a dry cell for which a potentiometer is balanced when  , while an alkaline standard cell with an emf of 1.600 V requires  to balance the potentiometer.

59. When an unknown resistance  is placed in a Wheatstone bridge, it is possible to balance the bridge by adjusting  to be  . What is  if 

60. To what value must you adjust  to balance a Wheatstone bridge, if the unknown resistance  is  is  , and  is 

61. (a) What is the unknown  in a potentiometer that balances when  is  , and balances when  is  for a standard 3.000-V emf? (b) The same  is placed in the same potentiometer, which now balances when  is  for a standard emf of  At what resistance  will the potentiometer balance?

62. Suppose you want to measure resistances in the range from  to  using a Wheatstone bridge that has  . Over what range should  be adjustable?

# 21.6 DC Circuits Containing Resistors and Capacitors

63. The timing device in an automobile’s intermittent wiper system is based on an  time constant and utilizes a  capacitor and a variable resistor. Over what range must  be made to vary to achieve time constants from 2.00 to 64. A heart pacemaker fires 72 times a minute, each time a 25.0-nF capacitor is charged (by a battery in series with a resistor) to 0.632 of its full voltage. What is the value of the resistance?

65. The duration of a photographic flash is related to an  time constant, which is  for a certain camera. (a) If the resistance of the flash lamp is  during discharge, what is the size of the capacitor supplying its energy? (b) What is the time constant for charging the capacitor, if the charging resistance is 

66. A 2.00- and a  capacitor can be connected in series or parallel, as can a 25.0- and a  resistor. Calculate the four  time constants possible from connecting the resulting capacitance and resistance in series.

67. After two time constants, what percentage of the final voltage, emf, is on an initially uncharged capacitor  , charged through a resistance 

68. A resistor, an uncharged  capacitor, and a 6.16-V emf are connected in series. (a) What is the initial current? (b) What is the  time constant? (c) What is the current after one time constant? (d) What is the voltage on the capacitor after one time constant?

69. A heart defibrillator being used on a patient has an time constant of  due to the resistance of the patient and the capacitance of the defibrillator. (a) If the defibrillator has an  capacitance, what is the resistance of the path through the patient? (You may neglect the capacitance of the patient and the resistance of the defibrillator.) (b) If the initial voltage is 12.0  , how long does it take to decline to  ?

70. An ECG monitor must have an  time constant less than  to be able to measure variations in voltage over small time intervals. (a) If the resistance of the circuit (due mostly to that of the patient’s chest) is  , what is the maximum capacitance of the circuit? (b) Would it be difficult in practice to limit the capacitance to less than the value found in (a)?

71. Figure 21.53 shows how a bleeder resistor is used to discharge a capacitor after an electronic device is shut off, allowing a person to work on the electronics with less risk of shock. (a) What is the time constant? (b) How long will it take to reduce the voltage on the capacitor to   of  ) of its full value once discharge begins? (c) If the capacitor is charged to a voltage  through a  resistance, calculate the time it takes to rise to  (This is about two time constants.)

  
FIGURE 21.53

72. Using the exact exponential treatment, find how much time is required to discharge a  capacitor through a resistor down to  of its original voltage.

73. Using the exact exponential treatment, find how much time is required to charge an initially uncharged 100-pF capacitor through a resistor to  of its final voltage.

74. Integrated Concepts If you wish to take a picture of a bullet traveling at  , then a very brief flash of light produced by an  discharge through a flash tube can limit blurring. Assuming  of motion during one  constant is acceptable, and given that the flash is driven by a  capacitor, what is the resistance in the flash tube?

75. Integrated Concepts A flashing lamp in a Christmas earring is based on an  discharge of a capacitor through its resistance. The effective duration of the flash is 0.250 s, during which it produces an average 0.500 W from an average  (a) What energy does it dissipate? (b) How much charge moves through the lamp? (c) Find the capacitance. (d) What is the resistance of the lamp?76. Integrated Concepts

A  capacitor charged to  is discharged through a  resistor. (a) Find the time constant. (b) Calculate the temperature increase of the resistor, given that its mass is 2.50  and its specific heat is  , noting that most of the thermal energy is retained in the short time of the discharge. (c) Calculate the new resistance, assuming it is pure carbon. (d) Does this change in resistance seem significant?

77. Unreasonable Results (a) Calculate the capacitance needed to get an  time constant of  with a resistor. (b) What is unreasonable about this result? (c) Which assumptions are responsible?

78. Construct Your Own Problem Consider a camera’s flash unit. Construct a problem in which you calculate the size of the capacitor that stores energy for the flash lamp. Among the things to be considered are the voltage applied to the capacitor, the energy needed in the flash and the associated charge needed on the capacitor, the resistance of the flash lamp during discharge, and the desired  time constant.

79. Construct Your Own Problem

Consider a rechargeable lithium cell that is to be used to power a camcorder. Construct a problem in which you calculate the internal resistance of the cell during normal operation. Also, calculate the minimum voltage output of a battery charger to be used to recharge your lithium cell. Among the things to be considered are the emf and useful terminal voltage of a lithium cell and the current it should be able to supply to a camcorder.

80. Critical Thinking A circuit has a voltage source producing  and a  resistor. (a) If the circuit contains nothing else, how much power is dissipated by the resistor? (b) A second  resistor is added in parallel to the first resistor. Now how much power is dissipated by the resistors? (c) Now place the two resistors in series. How much power is dissipated by the resistors? (d) Why would a parallel arrangement of resistors dissipate more power than a series arrangement of resistors of the same value? (e) Which delivers more energy in a given time period, the parallel combination of resistors, the series combination of resistors, or is the energy delivered in a given time period the same?