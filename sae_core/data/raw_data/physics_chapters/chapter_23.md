# Chapter 23 - Electromagnetic Induction, AC Circuits, and Electrical Technologies

  
FIGURE 23.1 These wind turbines in the Thames Estuary in the UK are an example of induction at work. Wind pushes the blades of the turbine, spinning a shaft attached to magnets. The magnets spin around a conductive coil, inducing an electric current in the coil, and eventually feeding the electrical grid. (credit: modification of work by Petr Kratochvil)

# CHAPTER OUTLINE

23.1 Induced Emf and Magnetic Flux   
23.2 Faraday’s Law of Induction: Lenz’s Law   
23.3 Motional Emf   
23.4 Eddy Currents and Magnetic Damping   
23.5 Electric Generators   
23.6 Back Emf   
23.7 Transformers   
23.8 Electrical Safety: Systems and Devices   
23.9 Inductance   
23.10 RL Circuits   
23.11 Reactance, Inductive and Capacitive   
23.12 RLC Series AC Circuits

# INTRODUCTION TO ELECTROMAGNETIC INDUCTION, AC CIRCUITS AND ELECTRICAL TECHNOLOGIES

Nature’s displays of symmetry are beautiful and alluring. A butterfly’s wings exhibit an appealing symmetry in a complex system. (See Figure 23.2.) The laws of physics display symmetries at the most basic level—these symmetries are a source of wonder and imply deeper meaning. Since we place a high value on symmetry, we look for it when we explore nature. The remarkable thing is that we find it.  
FIGURE 23.2 Physics, like this butterfly, has inherent symmetries. (credit: Thomas Bresson)

The hint of symmetry between electricity and magnetism found in the preceding chapter will be elaborated upon in this chapter. Specifically, we know that a current creates a magnetic field. If nature is symmetric here, then perhaps a magnetic field can create a current. The Hall effect is a voltage caused by a magnetic force. That voltage could drive a current. Historically, it was very shortly after Oersted discovered currents cause magnetic fields that other scientists asked the following question: Can magnetic fields cause currents? The answer was soon found by experiment to be yes. In 1831, some 12 years after Oersted’s discovery, the English scientist Michael Faraday (1791–1862) and the American scientist Joseph Henry (1797–1878) independently demonstrated that magnetic fields can produce currents. The basic process of generating emfs (electromotive force) and, hence, currents with magnetic fields is known as induction; this process is also called magnetic induction to distinguish it from charging by induction, which utilizes the Coulomb force.

Today, currents induced by magnetic fields are essential to our technological society. The ubiquitous generator—found in automobiles, on bicycles, in nuclear power plants, and so on—uses magnetism to generate current. Other devices that use magnetism to induce currents include pickup coils in electric guitars, transformers of every size, certain microphones, airport security gates, and damping mechanisms on sensitive chemical balances. Not so familiar perhaps, but important nevertheless, is that the behavior of AC circuits depends strongly on the effect of magnetic fields on currents.

Click to view content (https://openstax.org/books/college-physics-2e/pages/23-introduction-to-electromagnetic  
induction-ac-circuits-and-electrical-technologies)   
23.1 Induced Emf and Magnetic Flux

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Calculate the flux of a uniform magnetic field through a loop of arbitrary orientation. Describe methods to produce an electromotive force (emf) with a magnetic field or magnet and a loop of wire.

The apparatus used by Faraday to demonstrate that magnetic fields can create currents is illustrated in Figure 23.3. When the switch is closed, a magnetic field is produced in the coil on the top part of the iron ring and transmitted to the coil on the bottom part of the ring. The galvanometer is used to detect any current induced in the coil on the bottom. It was found that each time the switch is closed, the galvanometer detects a current in one direction in the coil on the bottom. (You can also observe this in a physics lab.) Each time the switch is opened, the galvanometer detects a current in the opposite direction. Interestingly, if the switch remains closed or open for any length of time, there is no current through the galvanometer. Closing and opening the switch induces the current. It is the change in magnetic field that creates the current. More basic than the current that flows is the emf that causes it. The current is a result of an emf induced by a changing magnetic field, whether or not there is a path for current to flow.  
FIGURE 23.3 Faraday’s apparatus for demonstrating that a magnetic field can produce a current. A change in the field produced by the top coil induces an emf and, hence, a current in the bottom coil. When the switch is opened and closed, the galvanometer registers currents in opposite directions. No current flows through the galvanometer when the switch remains closed or open.

An experiment easily performed and often done in physics labs is illustrated in Figure 23.4. An emf is induced in the coil when a bar magnet is pushed in and out of it. Emfs of opposite signs are produced by motion in opposite directions, and the emfs are also reversed by reversing poles. The same results are produced if the coil is moved rather than the magnet—it is the relative motion that is important. The faster the motion, the greater the emf, and there is no emf when the magnet is stationary relative to the coil.

  
FIGURE 23.4 Movement of a magnet relative to a coil produces emfs as shown. The same emfs are produced if the coil is moved relative to the magnet. The greater the speed, the greater the magnitude of the emf, and the emf is zero when there is no motion.

The method of inducing an emf used in most electric generators is shown in Figure 23.5. A coil is rotated in a magnetic field, producing an alternating current emf, which depends on rotation rate and other factors that will be explored in later sections. Note that the generator is remarkably similar in construction to a motor (another symmetry).  
FIGURE 23.5 Rotation of a coil in a magnetic field produces an emf. This is the basic construction of a generator, where work done to turn the coil is converted to electric energy. Note the generator is very similar in construction to a motor.

So we see that changing the magnitude or direction of a magnetic field produces an emf. Experiments revealed that there is a crucial quantity called the magnetic flux,  , given by



where  is the magnetic field strength over an area  , at an angle  with the perpendicular to the area as shown in Figure 23.6. Any change in magnetic flux  induces an emf. This process is defined to be electromagnetic induction. Units of magnetic flux  are  . As seen in Figure 23.6,  cos  , which is the component of  perpendicular to the area  . Thus magnetic flux is  , the product of the area and the component of the magnetic field perpendicular to it.

  
FIGURE 23.6 Magnetic flux  is related to the magnetic field and the area over which it exists. The flux  cos  is related to induction; any change in  induces an emf.

All induction, including the examples given so far, arises from some change in magnetic flux  . For example, Faraday changed  and hence  when opening and closing the switch in his apparatus (shown in Figure 23.3). This is also true for the bar magnet and coil shown in Figure 23.4. When rotating the coil of a generator, the angle  and, hence,  is changed. Just how great an emf and what direction it takes depend on the change in  and how rapidly the change is made, as examined in the next section.# 23.2 Faraday’s Law of Induction: Lenz’s Law

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Calculate emf, current, and magnetic fields using Faraday’s Law. Explain the physical results of Lenz’s Law

# Faraday’s and Lenz’s Law

Faraday’s experiments showed that the emf induced by a change in magnetic flux depends on only a few factors. First, emf is directly proportional to the change in flux  . Second, emf is greatest when the change in time  is smallest—that is, emf is inversely proportional to  . Finally, if a coil has  turns, an emf will be produced that is  times greater than for a single coil, so that emf is directly proportional to  . The equation for the emf induced by a change in magnetic flux is



This relationship is known as Faraday’s law of induction. The units for emf are volts, as is usual.

The minus sign in Faraday’s law of induction is very important. The minus means that the emf creates a current I and magnetic field B that oppose the change in flux  —this is known as Lenz's law. The direction (given by the minus sign) of the emfis so important that it is called Lenz’s law after the Russian Heinrich Lenz (1804–1865), who, like Faraday and Henry,independently investigated aspects of induction. Faraday was aware of the direction, but Lenz stated it so clearly that he is credited for its discovery. (See Figure 23.7.)

  
FIGURE 23.7 (a) When this bar magnet is thrust into the coil, the strength of the magnetic field increases in the coil. The current induced in the coil creates another field, in the opposite direction of the bar magnet’s to oppose the increase. This is one aspect of Lenz’s  shown indeed opposes the change in flux and that the current direction shown is consistent with RHR-2.

# Problem-Solving Strategy for Lenz’s Law

To use Lenz’s law to determine the directions of the induced magnetic fields, currents, and emfs:

1. Make a sketch of the situation for use in visualizing and recording directions.   
2. Determine the direction of the magnetic field B.   
3. Determine whether the flux is increasing or decreasing.   
4. Now determine the direction of the induced magnetic field B. It opposes the change in flux by adding orsubtracting from the original field.

5. Use RHR-2 to determine the direction of the induced current I that is responsible for the induced magnetic field B.   
6. The direction (or polarity) of the induced emf will now drive a current in this direction and can be represented as current emerging from the positive terminal of the emf and returning to its negative terminal.

For practice, apply these steps to the situations shown in Figure 23.7 and to others that are part of the following text material.

# Applications of Electromagnetic Induction

There are many applications of Faraday’s Law of induction, as we will explore in this chapter and others. At this juncture, let us mention several that have to do with data storage and magnetic fields. A very important application has to do with audio and video recording tapes. A plastic tape, coated with iron oxide, moves past a recording head. This recording head is basically a round iron ring about which is wrapped a coil of wire—an electromagnet (Figure 23.8). A signal in the form of a varying input current from a microphone or camera goes to the recording head. These signals (which are a function of the signal amplitude and frequency) produce varying magnetic fields at the recording head. As the tape moves past the recording head, the magnetic field orientations of the iron oxide molecules on the tape are changed thus recording the signal. In the playback mode, the magnetized tape is run past another head, similar in structure to the recording head. The different magnetic field orientations of the iron oxide molecules on the tape induces an emf in the coil of wire in the playback head. This signal then is sent to a loudspeaker or video player.

  
FIGURE 23.8 Recording and playback heads used with audio and video magnetic tapes. (credit: Steve Jurvetson)

Similar principles apply to computer hard drives, except at a much faster rate. Here recordings are on a coated, spinning disk. Read heads historically were made to work on the principle of induction. However, the input information is carried in digital rather than analog form – a series of 0’s or 1’s are written upon the spinning hard drive. Today, most hard drive readout devices do not work on the principle of induction, but use a technique known as giant magnetoresistance. (The discovery that weak changes in a magnetic field in a thin film of iron and chromium could bring about much larger changes in electrical resistance was one of the first large successes of nanotechnology.) Another application of induction is found on the magnetic stripe on the back of your personal credit card as used at the grocery store or the ATM machine. This works on the same principle as the audio or video tape mentioned in the last paragraph in which a head reads personal information from your card.

Another application of electromagnetic induction is when electrical signals need to be transmitted across a barrier. Consider the cochlear implant shown below. Sound is picked up by a microphone on the outside of the skull and is used to set up a varying magnetic field. A current is induced in a receiver secured in the bone beneath the skin and transmitted to electrodes in the inner ear. Electromagnetic induction can be used in other instances where electric signals need to be conveyed across various media.  
FIGURE 23.9 Electromagnetic induction used in transmitting electric currents across mediums. The device on the baby’s head induces an electrical current in a receiver secured in the bone beneath the skin. (credit: Bjorn Knetsch)

Another contemporary area of research in which electromagnetic induction is being successfully implemented (and with substantial potential) is transcranial magnetic simulation. A host of disorders, including depression and hallucinations can be traced to irregular localized electrical activity in the brain. In transcranial magnetic Weak electric currents are induced in the identified sites and can result in recovery of electrical functioning in the brain tissue.

u cause of sudden infant deaths [SID]). In such individuals, breath can stop repeatedly during their sleep. A cessation of more than 20 seconds can be very dangerous. Stroke, heart failure, and tiredness are just some of the possible consequences for a person having sleep apnea. The concern in infants is the stopping of breath for these longer times. One type of monitor to alert parents when a child is not breathing uses electromagnetic induction. A wire wrapped around the infant’s chest has an alternating current running through it. The expansion and contraction of the infant’s chest as the infant breathes changes the area through the coil. A pickup coil located nearby has an alternating current induced in it due to the changing magnetic field of the initial wire. If the child stops breathing, there will be a change in the induced current, and so a parent can be alerted.

# Making Connections: Conservation of Energy

Lenz’s law is a manifestation of the conservation of energy. The induced emf produces a current that opposes the change in flux, because a change in flux means a change in energy. Energy can enter or leave, but not instantaneously. Lenz’s law is a consequence. As the change begins, the law says induction opposes and, thus, slows the change. In fact, if the induced emf were in the same direction as the change in flux, there would be a positive feedback that would give us free energy from no apparent source—conservation of energy would be violated.

# EXAMPLE 23.1

# Calculating Emf: How Great Is the Induced Emf?

Calculate the magnitude of the induced emf when the magnet in Figure 23.7(a) is thrust into the coil, given the following information: the single loop coil has a radius of 6.00 cm and the average value of  cos  (this is given, since the bar magnet’s field is complex) increases from 0.0500 T to  in  .

# Strategy

To find the magnitude of emf, we use Faraday’s law of induction as stated by  , but without the minus sign that indicates direction:



# Solution

We are given that  and  , but we must determine the change in flux  before we can find emf.Since the area of the loop is fixed, we see that



Now  , since it was given that  cos  changes from 0.0500 to 0.250 T. The area of the loop is  . Thus,



Entering the determined values into the expression for emf gives



# Discussion

While this is an easily measured voltage, it is certainly not large enough for most practical applications. More loops in the coil, a stronger magnet, and faster movement make induction the practical source of voltages that it is.

# PHET EXPLORATIONS

# Faraday's Electromagnetic Lab

Play with a bar magnet and coils to learn about Faraday's law. Move a bar magnet near one or two coils to make a light bulb glow. View the magnetic field lines. A meter shows the direction and magnitude of the current. View the magnetic field lines or use a meter to show the direction and magnitude of the current. You can also play with electromagnets, generators and transformers!

Click to view content (https://openstax.org/l/Faraday-EM-lab).

# 23.3 Motional Emf

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Calculate emf, force, magnetic field, and work due to the motion of an object in a magnetic field.

As we have seen, any change in magnetic flux induces an emf opposing that change—a process known as induction. Motion is one of the major causes of induction. For example, a magnet moved toward a coil induces an emf, and a coil moved toward a magnet produces a similar emf. In this section, we concentrate on motion in a magnetic field that is stationary relative to the Earth, producing what is loosely called motional emf.

One situation where motional emf occurs is known as the Hall effect and has already been examined. Charges moving in a magnetic field experience the magnetic force  sin  , which moves opposite charges in opposite directions and produces an  . We saw that the Hall effect has applications, including measurements of  and  . We will now see that the Hall effect is one aspect of the broader phenomenon of induction, and we will find that motional emf can be used as a power source.

Consider the situation shown in Figure 23.10. A rod is moved at a speed  along a pair of conducting rails separated by a distance  in a uniform magnetic field  . The rails are stationary relative to  and are connected to a stationary resistor  . The resistor could be anything from a light bulb to a voltmeter. Consider the area enclosed by the moving rod, rails, and resistor.  is perpendicular to this area, and the area is increasing as the rod moves. Thus the magnetic flux enclosed by the rails, rod, and resistor is increasing. When flux changes, an emf is induced according to Faraday’s law of induction.  
FIGURE 23.10 (a) A motional  is induced between the rails when this rod moves to the right in the uniform magnetic field. The magnetic field  is into the page, perpendicular to the moving rod and rails and, hence, to the area enclosed by them. (b) Lenz’s law gives the directions of the induced field and current, and the polarity of the induced emf. Since the flux is increasing, the induced field is in the opposite direction, or out of the page. RHR-2 gives the current direction shown, and the polarity of the rod will drive such a current. RHR-1 also indicates the same polarity for the rod. (Note that the script E symbol used in the equivalent circuit at the bottom of part (b) represents emf.)

To find the magnitude of emf induced along the moving rod, we use Faraday’s law of induction without the sign:



Here and below, “emf” implies the magnitude of the emf. In this equation,  and the flux  cos  . We have  and  , since  is perpendicular to  . Now  , since  is uniform. Note that the area swept out by the rod is  . Entering these quantities into the expression for emf yields



inally, note that  , the velocity of the rod. Entering this into the last expression shows that

is the motional emf. This is the same expression given for the Hall effect previously.# Making Connections: Unification of Forces

There are many connections between the electric force and the magnetic force. The fact that a moving electric field produces a magnetic field and, conversely, a moving magnetic field produces an electric field is part of why electric and magnetic forces are now considered to be different manifestations of the same force. This classic unification of electric and magnetic forces into what is called the electromagnetic force is the inspiration for contemporary efforts to unify other basic forces.

To find the direction of the induced field, the direction of the current, and the polarity of the induced emf, we apply Lenz’s law as explained in Faraday's Law of Induction: Lenz's Law. (See Figure 23.10(b).) Flux is increasing, since the area enclosed is increasing. Thus the induced field must oppose the existing one and be out of the page. And so the RHR-2 requires that I be counterclockwise, which in turn means the top of the rod is positive as shown.

Motional emf also occurs if the magnetic field moves and the rod (or other object) is stationary relative to the Earth (or some observer). We have seen an example of this in the situation where a moving magnet induces an emf in a stationary coil. It is the relative motion that is important. What is emerging in these observations is a connection between magnetic and electric fields. A moving magnetic field produces an electric field through its induced emf. We already have seen that a moving electric field produces a magnetic field—moving charge implies moving electric field and moving charge produces a magnetic field.

Motional emfs in the Earth’s weak magnetic field are not ordinarily very large, or we would notice voltage along metal rods, such as a screwdriver, during ordinary motions. For example, a simple calculation of the motional emf of a 1 m rod moving at  perpendicular to the Earth’s field gives  This small value is consistent with experience. There is a spectacular exception, however. In 1992 and 1996, attempts were made with the space shuttle to create large motional emfs. The Tethered Satellite was to be let out on a  length of wire as shown in Figure 23.11, to create a  emf by moving at orbital speed through the Earth’s field. This emf could be used to convert some of the shuttle’s kinetic and potential energy into electrical energy if a complete circuit could be made. To complete the circuit, the stationary ionosphere was to supply a return path for the current to flow. (The ionosphere is the rarefied and partially ionized atmosphere at orbital altitudes. It conducts because of the ionization. The ionosphere serves the same function as the stationary rails and connecting resistor in Figure 23.10, without which there would not be a complete circuit.) Drag on the current in the cable due to the magnetic force  sin  does the work that reduces the shuttle’s kinetic and potential energy and allows it to be converted to electrical energy. The tests were both unsuccessful. In the first, the cable hung up and could only be extended a couple of hundred meters; in the second, the cable broke when almost fully extended. Example 23.2 indicates feasibility in principle.# EXAMPLE 23.2

# Calculating the Large Motional Emf of an Object in Orbit

  
FIGURE 23.11 Motional emf as electrical power conversion for the space shuttle is the motivation for the Tethered Satellite experiment. A 5 kV emf was predicted to be induced in the  long tether while moving at orbital speed in the Earth’s magnetic field. The circuit is completed by a return path through the stationary ionosphere.

Calculate the motional emf induced along a  long conductor moving at an orbital speed of  perpendicular to the Earth’s  magnetic field.

# Strategy

This is a straightforward application of the expression for motional emf— 

# Solution

Entering the given values into  gives



# Discussion

The value obtained is greater than the  measured voltage for the shuttle experiment, since the actual orbital motion of the tether is not perpendicular to the Earth’s field. The  value is the maximum emf obtained when  and  .

# 23.4 Eddy Currents and Magnetic Damping

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Explain the magnitude and direction of an induced eddy current, and the effect this will have on the object it is induced in.   
Describe several applications of magnetic damping.

# Eddy Currents and Magnetic Damping

As discussed in Motional Emf, motional emf is induced when a conductor moves in a magnetic field or when a magnetic field moves relative to a conductor. If motional emf can cause a current loop in the conductor, we refer tothat current as an eddy current. Eddy currents can produce significant drag, called magnetic damping, on the motion involved. Consider the apparatus shown in Figure 23.12, which swings a pendulum bob between the poles of a strong magnet. (This is another favorite physics lab activity.) If the bob is metal, there is significant drag on the bob as it enters and leaves the field, quickly damping the motion. If, however, the bob is a slotted metal plate, as shown in Figure 23.12(b), there is a much smaller effect due to the magnet. There is no discernible effect on a bob made of an insulator. Why is there drag in both directions, and are there any uses for magnetic drag?

  
FIGURE 23.12 A common physics demonstration device for exploring eddy currents and magnetic damping. (a) The motion of a metal pendulum bob swinging between the poles of a magnet is quickly damped by the action of eddy currents. (b) There is little effect on the motion of a slotted metal bob, implying that eddy currents are made less effective. (c) There is also no magnetic damping on a nonconducting bob, since the eddy currents are extremely small.

Figure 23.13 shows what happens to the metal plate as it enters and leaves the magnetic field. In both cases, it experiences a force opposing its motion. As it enters from the left, flux increases, and so an eddy current is set up (Faraday’s law) in the counterclockwise direction (Lenz’s law), as shown. Only the right-hand side of the current loop is in the field, so that there is an unopposed force on it to the left (RHR-1). When the metal plate is completely inside the field, there is no eddy current if the field is uniform, since the flux remains constant in this region. But when the plate leaves the field on the right, flux decreases, causing an eddy current in the clockwise direction that, again, experiences a force to the left, further slowing the motion. A similar analysis of what happens when the plate swings from the right toward the left shows that its motion is also damped when entering and leaving the field.

  
FIGURE 23.13 A more detailed look at the conducting plate passing between the poles of a magnet. As it enters and leaves the field, the change in flux produces an eddy current. Magnetic force on the current loop opposes the motion. There is no current and no magnetic drag when the plate is completely inside the uniform field.

When a slotted metal plate enters the field, as shown in Figure 23.14, an emf is induced by the change in flux, but it is less effective because the slots limit the size of the current loops. Moreover, adjacent loops have currents in opposite directions, and their effects cancel. When an insulating material is used, the eddy current is extremely small, and so magnetic damping on insulators is negligible. If eddy currents are to be avoided in conductors, then they can be slotted or constructed of thin layers of conducting material separated by insulating sheets.  
FIGURE 23.14 Eddy currents induced in a slotted metal plate entering a magnetic field form small loops, and the forces on them tend to cancel, thereby making magnetic drag almost zero.

# Applications of Magnetic Damping

One use of magnetic damping is found in sensitive laboratory balances. To have maximum sensitivity and accuracy, the balance must be as friction-free as possible. But if it is friction-free, then it will oscillate for a very long time. Magnetic damping is a simple and ideal solution. With magnetic damping, drag is proportional to speed and becomes zero at zero velocity. Thus the oscillations are quickly damped, after which the damping force disappears, allowing the balance to be very sensitive. (See Figure 23.15.) In most balances, magnetic damping is accomplished with a conducting disc that rotates in a fixed field.

  
FIGURE 23.15 Magnetic damping of this sensitive balance slows its oscillations. Since Faraday’s law of induction gives the greatest effect for the most rapid change, damping is greatest for large oscillations and goes to zero as the motion stops.

Since eddy currents and magnetic damping occur only in conductors, recycling centers can use magnets to separate metals from other materials. Trash is dumped in batches down a ramp, beneath which lies a powerful magnet. Conductors in the trash are slowed by magnetic damping while nonmetals in the trash move on, separating from the metals. (See Figure 23.16.) This works for all metals, not just ferromagnetic ones. A magnet can separate out the ferromagnetic materials alone by acting on stationary trash.  
FIGURE 23.16 Metals can be separated from other trash by magnetic drag. Eddy currents and magnetic drag are created in the metals sent down this ramp by the powerful magnet beneath it. Nonmetals move on.

Other major applications of eddy currents are in metal detectors and braking systems in trains and roller coasters. Portable metal detectors (Figure 23.17) consist of a primary coil carrying an alternating current and a secondary coil in which a current is induced. An eddy current will be induced in a piece of metal close to the detector which will cause a change in the induced current within the secondary coil, leading to some sort of signal like a shrill noise. Braking using eddy currents is safer because factors such as rain do not affect the braking and the braking is smoother. However, eddy currents cannot bring the motion to a complete stop, since the force produced decreases with speed. Thus, speed can be reduced from say  to  , but another form of braking is needed to completely stop the vehicle. Generally, powerful rare earth magnets such as neodymium magnets are used in roller coasters. Figure 23.18 shows rows of magnets in such an application. The vehicle has metal fins (normally containing copper) which pass through the magnetic field slowing the vehicle down in much the same way as with the pendulum bob shown in Figure 23.12.

  
FIGURE 23.17 A soldier uses a metal detector to search for explosives and weapons. (credit: U.S. Army)  
FIGURE 23.18 The rows of rare earth magnets (protruding horizontally) are used for magnetic braking in roller coasters. (credit: Stefan Scheer, Wikimedia Commons)

Induction cooktops have electromagnets under their surface. The magnetic field is varied rapidly producing eddy currents in the base of the pot, causing the pot and its contents to increase in temperature. Induction cooktops have high efficiencies and good response times but the base of the pot needs to be ferromagnetic, iron or steel for induction to work.

# 23.5 Electric Generators

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

• Calculate the emf induced in a generator. Calculate the peak emf which can be induced in a particular generator system.

Electric generators induce an emf by rotating a coil in a magnetic field, as briefly discussed in Induced Emf and Magnetic Flux. We will now explore generators in more detail. Consider the following example.

# EXAMPLE 23.3

# Calculating the Emf Induced in a Generator Coil

The generator coil shown in Figure 23.19 is rotated through one-fourth of a revolution (from  to  ) in  . The 200-turn circular coil has a  radius and is in a uniform  magnetic field. What is the average emf induced?  
FIGURE 23.19 When this generator coil is rotated through one-fourth of a revolution, the magnetic flux  changes from its maximum to zero, inducing an emf.

# Strategy

We use Faraday’s law of induction to find the average emf induced over a time  :



We know that  and  , and so we must determine the change in flux  to find emf.

# Solution

Since the area of the loop and the magnetic field strength are constant, we see that



Now,  , since it was given that  goes from  to  . Thus  , and



The area of the loop is  . Entering this value gives



# Discussion

This is a practical average value, similar to the  used in household power.

The emf calculated in Example 23.3 is the average over one-fourth of a revolution. What is the emf at any given instant? It varies with the angle between the magnetic field and a perpendicular to the coil. We can get an expression for emf as a function of time by considering the motional emf on a rotating rectangular coil of width  and height  in a uniform magnetic field, as illustrated in Figure 23.20.  
FIGURE 23.20 A generator with a single rectangular coil rotated at constant angular velocity in a uniform magnetic field produces an emf that varies sinusoidally in time. Note the generator is similar to a motor, except the shaft is rotated to produce a current rather than the other way around.

Charges in the wires of the loop experience the magnetic force, because they are moving in a magnetic field. Charges in the vertical wires experience forces parallel to the wire, causing currents. But those in the top and bottom segments feel a force perpendicular to the wire, which does not cause a current. We can thus find the induced emf by considering only the side wires. Motional emf is given to be  , where the velocity v is perpendicular to the magnetic field  . Here the velocity is at an angle  with  , so that its component perpendicular to  is  sin  (see Figure 23.20). Thus in this case the emf induced on each side is  sin  , and they are in the same direction. The total emf around the loop is then



This expression is valid, but it does not give emf as a function of time. To find the time dependence of emf, we assume the coil rotates at a constant angular velocity  . The angle  is related to angular velocity by  , so that



Now, linear velocity  is related to angular velocity  by  . Here  , so that  , and



Noting that the area of the loop is  , and allowing for  loops, we find that



is the emf induced in a generator coil of  turns and area  rotating at a constant angular velocity  in a uniform magnetic field  . This can also be expressed as



where



is the maximum (peak) emf. Note that the frequency of the oscillation is  , and the period is  Figure 23.21 shows a graph of emf as a function of time, and it now seems reasonable that AC voltage is sinusoidal.  
FIGURE 23.21 The emf of a generator is sent to a light bulb with the system of rings and brushes shown. The graph gives the emf of the generator as a function of time.  is the peak emf. The period is  , where  is the frequency. Note that the script E stands for emf.

The fact that the peak emf,  , makes good sense. The greater the number of coils, the larger their area, and the stronger the field, the greater the output voltage. It is interesting that the faster the generator is spun (greater  ), the greater the emf. This is noticeable on bicycle generators—at least the cheaper varieties. One of the authors as a juvenile found it amusing to ride his bicycle fast enough to burn out his lights, until he had to ride home lightless one dark night.

Figure 23.22 shows a scheme by which a generator can be made to produce pulsed DC. More elaborate arrangements of multiple coils and split rings can produce smoother DC, although electronic rather than mechanical means are usually used to make ripple-free DC.

  
FIGURE 23.22 Split rings, called commutators, produce a pulsed DC emf output in this configuration.

# EXAMPLE 23.4

# Calculating the Maximum Emf of a Generator

Calculate the maximum emf,  , of the generator that was the subject of Example 23.3.

# Strategy

Once  , the angular velocity, is determined,  can be used to find  . All other quantities areknown.

# Solution

Angular velocity is defined to be the change in angle per unit time:



One-fourth of a revolution is  radians, and the time is 0.0150 s; thus,



 is exactly 1000 rpm. We substitute this value for  and the information from the previous example into  , yielding



# Discussion

The maximum emf is greater than the average emf of 131 V found in the previous example, as it should be.

In real life, electric generators look a lot different than the figures in this section, but the principles are the same. The source of mechanical energy that turns the coil can be falling water (hydropower), steam produced by the burning of fossil fuels, or the kinetic energy of wind. Figure 23.23 shows a cutaway view of a steam turbine; steam moves over the blades connected to the shaft, which rotates the coil within the generator.

  
FIGURE 23.23 Steam turbine/generator. The steam produced by burning coal impacts the turbine blades, turning the shaft which is connected to the generator. (credit: Nabonaco, Wikimedia Commons)

Generators illustrated in this section look very much like the motors illustrated previously. This is not coincidental. In fact, a motor becomes a generator when its shaft rotates. Certain early automobiles used their starter motor as a generator. In Back Emf, we shall further explore the action of a motor as a generator.

# 23.6 Back Emf

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Explain what back emf is and how it is induced.

It has been noted that motors and generators are very similar. Generators convert mechanical energy into electrical energy, whereas motors convert electrical energy into mechanical energy. Furthermore, motors and generators have the same construction. When the coil of a motor is turned, magnetic flux changes, and an emf (consistent with Faraday’s law of induction) is induced. The motor thus acts as a generator whenever its coil rotates. This will happenwhether the shaft is turned by an external input, like a belt drive, or by the action of the motor itself. That is, when a motor is doing work and its shaft is turning, an emf is generated. Lenz’s law tells us the emf opposes any change, so that the input emf that powers the motor will be opposed by the motor’s self-generated emf, called the back emf of the motor. (See Figure 23.24.)

  
FIGURE 23.24 The coil of a DC motor is represented as a resistor in this schematic. The back emf is represented as a variable emf that opposes the one driving the motor. Back emf is zero when the motor is not turning, and it increases proportionally to the motor’s angular velocity.

Back emf is the generator output of a motor, and so it is proportional to the motor’s angular velocity  . It is zero when the motor is first turned on, meaning that the coil receives the full driving voltage and the motor draws maximum current when it is on but not turning. As the motor turns faster and faster, the back emf grows, always opposing the driving emf, and reduces the voltage across the coil and the amount of current it draws. This effect is noticeable in a number of situations. When a vacuum cleaner, refrigerator, or washing machine is first turned on, lights in the same circuit dim briefly due to the  drop produced in feeder lines by the large current drawn by the motor. When a motor first comes on, it draws more current than when it runs at its normal operating speed. When a mechanical load is placed on the motor, like an electric wheelchair going up a hill, the motor slows, the back emf drops, more current flows, and more work can be done. If the motor runs at too low a speed, the larger current can overheat it (via resistive power in the coil,  , perhaps even burning it out. On the other hand, if there is no mechanical load on the motor, it will increase its angular velocity  until the back emf is nearly equal to the driving emf. Then the motor uses only enough energy to overcome friction.

Consider, for example, the motor coils represented in Figure 23.24. The coils have a  equivalent resistance and are driven by a  emf. Shortly after being turned on, they draw a current   
 and, thus, dissipate  of energy as heat transfer. Under normal operating conditions for this motor, suppose the back emf is  . Then at operating speed, the total voltage across the coils is   minus the  back emf), and the current drawn is   
  . Under normal load, then, the power dissipated is   
 . The latter will not cause a problem for this motor, whereas the former 5.76 kW would burn out the coils if sustained.

# 23.7 Transformers

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Explain how a transformer works. • Calculate voltage, current, and/or number of turns given the other quantities.

Transformers do what their name implies—they transform voltages from one value to another (The term voltage is used rather than emf, because transformers have internal resistance). For example, many cell phones, laptops, video games, and power tools and small appliances have a transformer built into their plug-in unit (like that in Figure 23.25) that changes  or 240 V AC into whatever voltage the device uses. Transformers are also used at several points in the power distribution systems, such as illustrated in Figure 23.26. Power is sent long distances at high voltages, because less current is required for a given amount of power, and this means less line loss, as was discussed previously. But high voltages pose greater hazards, so that transformers are employed to produce lowervoltage at the user’s location.

  
FIGURE 23.25 The plug-in transformer has become increasingly familiar with the proliferation of electronic devices that operate on voltages other than common  AC. Most are in the 3 to  range. (credit: Shop Xtreme)

  
FIGURE 23.26 Transformers change voltages at several points in a power distribution system. Electric power is usually generated at greater than  , and transmitted long distances at voltages over 200 kV—sometimes as great as  —to limit energy losses. Local power distribution to neighborhoods or industries goes through a substation and is sent short distances at voltages ranging from 5 to  This is reduced to 120, 240, or  for safety at the individual user site.

The type of transformer considered in this text—see Figure 23.27—is based on Faraday’s law of induction and is very similar in construction to the apparatus Faraday used to demonstrate magnetic fields could cause currents. The two coils are called the primary and secondary coils. In normal use, the input voltage is placed on the primary, and the secondary produces the transformed output voltage. Not only does the iron core trap the magnetic field created by the primary coil, its magnetization increases the field strength. Since the input voltage is AC, a time-varying magnetic flux is sent to the secondary, inducing its AC output voltage.  
FIGURE 23.27 A typical construction of a simple transformer has two coils wound on a ferromagnetic core that is laminated to minimize eddy currents. The magnetic field created by the primary is mostly confined to and increased by the core, which transmits it to the secondary coil. Any change in current in the primary induces a current in the secondary.

For the simple transformer shown in Figure 23.27, the output voltage  depends almost entirely on the input voltage  and the ratio of the number of loops in the primary and secondary coils. Faraday’s law of induction for the secondary coil gives its induced output voltage  to be



where  is the number of loops in the secondary coil and  is the rate of change of magnetic flux. Note that the output voltage equals the induced emf  ), provided coil resistance is small (a reasonable assumption for transformers). The cross-sectional area of the coils is the same on either side, as is the magnetic field strength, and so  is the same on either side. The input primary voltage  is also related to changing flux by



The reason for this is a little more subtle. Lenz’s law tells us that the primary coil opposes the change in flux caused by the input voltage  , hence the minus sign (This is an example of self-inductance, a topic to be explored in some detail in later sections). Assuming negligible coil resistance, Kirchhoff’s loop rule tells us that the induced emf exactly equals the input voltage. Taking the ratio of these last two equations yields a useful relationship:



This is known as the transformer equation, and it simply states that the ratio of the secondary to primary voltages in a transformer equals the ratio of the number of loops in their coils.

The output voltage of a transformer can be less than, greater than, or equal to the input voltage, depending on the ratio of the number of loops in their coils. Some transformers even provide a variable output by allowing connection to be made at different points on the secondary coil. A step-up transformer is one that increases voltage, whereas a step-down transformer decreases voltage. Assuming, as we have, that resistance is negligible, the electrical power output of a transformer equals its input. This is nearly true in practice—transformer efficiency often exceeds  . Equating the power input and output,



Rearranging terms gives

Combining this with  , we find that



is the relationship between the output and input currents of a transformer. So if voltage increases, current decreases. Conversely, if voltage decreases, current increases.

# EXAMPLE 23.5

# Calculating Characteristics of a Step-Up Transformer

A portable x-ray unit has a step-up transformer, the  input of which is transformed to the  output needed by the  -ray tube. The primary has 50 loops and draws a current of 10.00 A when in use. (a) What is the number of loops in the secondary? (b) Find the current output of the secondary.

# Strategy and Solution for (a)

We solve  for  , the number of loops in the secondary, and enter the known values. This gives



# Discussion for (a)

A large number of loops in the secondary (compared with the primary) is required to produce such a large voltage.   
This would be true for neon sign transformers and those supplying high voltage inside TVs and CRTs.

# Strategy and Solution for (b)

We can similarly find the output current of the secondary by solving  for and entering known values. This gives



# Discussion for (b)

As expected, the current output is significantly less than the input. In certain spectacular demonstrations, very large voltages are used to produce long arcs, but they are relatively safe because the transformer output does not supply a large current. Note that the power input here is  This equals the power output  , as we assumed in the derivation of the equations used.

The fact that transformers are based on Faraday’s law of induction makes it clear why we cannot use transformers to change DC voltages. If there is no change in primary voltage, there is no voltage induced in the secondary. One possibility is to connect DC to the primary coil through a switch. As the switch is opened and closed, the secondary produces a voltage like that in Figure 23.28. This is not really a practical alternative, and AC is in common use wherever it is necessary to increase or decrease voltages.  
FIGURE 23.28 Transformers do not work for pure DC voltage input, but if it is switched on and off as on the top graph, the output will look something like that on the bottom graph. This is not the sinusoidal AC most AC appliances need.

# EXAMPLE 23.6

# Calculating Characteristics of a Step-Down Transformer

A battery charger meant for a series connection of ten nickel-cadmium batteries (total emf of 12.5 V DC) needs to have a 15.0 V output to charge the batteries. It uses a step-down transformer with a 200-loop primary and a  input. (a) How many loops should there be in the secondary coil? (b) If the charging current is 16.0 A, what is the input current?

# Strategy and Solution for (a)

You would expect the secondary to have a small number of loops. Solving  for and entering known values gives



# Strategy and Solution for (b)

The current input can be obtained by solving  for  and entering known values. This gives



# Discussion

The number of loops in the secondary is small, as expected for a step-down transformer. We also see that a small input current produces a larger output current in a step-down transformer. When transformers are used to operate large magnets, they sometimes have a small number of very heavy loops in the secondary. This allows the secondary to have low internal resistance and produce large currents. Note again that this solution is based on the assumption of  efficiency—or power out equals power in  )—reasonable for good transformers. In this case the primary and secondary power is 240 W. (Verify this for yourself as a consistency check.) Note that the NiCd batteries need to be charged from a DC power source (as would a  battery). So the AC output of thesecondary coil needs to be converted into DC. This is done using something called a rectifier, which uses devices called diodes that allow only a one-way flow of current.

Transformers have many applications in electrical safety systems, which are discussed in Electrical Safety: Systems and Devices.

# PHET EXPLORATIONS

# Generator

Generate electricity with a bar magnet! Discover the physics behind the phenomena by exploring magnets and how you can use them to make a bulb light.

Click to view content (https://openstax.org/l/28gen).

# 23.8 Electrical Safety: Systems and Devices

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Explain how various modern safety features in electric circuits work, with an emphasis on how induction is employed.

Electricity has two hazards. A thermal hazard occurs when there is electrical overheating. A shock hazard occurs when electric current passes through a person. Both hazards have already been discussed. Here we will concentrate on systems and devices that prevent electrical hazards.

Figure 23.29 shows the schematic for a simple AC circuit with no safety features. This is not how power is distributed in practice. Modern household and industrial wiring requires the three-wire system, shown schematically in Figure 23.30, which has several safety features. First is the familiar circuit breaker (or fuse) to prevent thermal overload. Second, there is a protective case around the appliance, such as a toaster or refrigerator. The case’s safety feature is that it prevents a person from touching exposed wires and coming into electrical contact with the circuit, helping prevent shocks.

  
FIGURE 23.29 Schematic of a simple AC circuit with a voltage source and a single appliance represented by the resistance . There are no safety features in this circuit.  
FIGURE 23.30 The three-wire system connects the neutral wire to the earth at the voltage source and user location, forcing it to be at zero volts and supplying an alternative return path for the current through the earth. Also grounded to zero volts is the case of the appliance. A circuit breaker or fuse protects against thermal overload and is in series on the active (live/hot) wire. Note that wire insulation colors vary with region and it is essential to check locally to determine which color codes are in use (and even if they were followed in the particular installation).

There are three connections to earth or ground (hereafter referred to as “earth/ground”) shown in Figure 23.30. Recall that an earth/ground connection is a low-resistance path directly to the earth. The two earth/ground connections on the neutral wire force it to be at zero volts relative to the earth, giving the wire its name. This wire is therefore safe to touch even if its insulation, usually white, is missing. The neutral wire is the return path for the current to follow to complete the circuit. Furthermore, the two earth/ground connections supply an alternative path through the earth, a good conductor, to complete the circuit. The earth/ground connection closest to the power source could be at the generating plant, while the other is at the user’s location. The third earth/ground is to the case of the appliance, through the green earth/ground wire, forcing the case, too, to be at zero volts. The live or hot o a more pictorial version of how the three-wire system is connected through a three-prong plug to an appliance.

  
FIGURE 23.31 The standard three-prong plug can only be inserted in one way, to assure proper function of the three-wire system.

A note on insulation color-coding: Insulating plastic is color-coded to identify live/hot, neutral and ground wires but these codes vary around the world. Live/hot wires may be brown, red, black, blue or grey. Neutral wire may be blue, black or white. Since the same color may be used for live/hot or neutral in different parts of the world, it is essential to determine the color code in your region. The only exception is the earth/ground wire which is often green but may be yellow or just bare wire. Striped coatings are sometimes used for the benefit of those who are colorblind.The three-wire system replaced the older two-wire system, which lacks an earth/ground wire. Under ordinary circumstances, insulation on the live/hot and neutral wires prevents the case from being directly in the circuit, so that the earth/ground wire may seem like double protection. Grounding the case solves more than one problem, however. The simplest problem is worn insulation on the live/hot wire that allows it to contact the case, as shown in Figure 23.32. Lacking an earth/ground connection (some people cut the third prong off the plug because they only have outdated two hole receptacles), a severe shock is possible. This is particularly dangerous in the kitchen, where a good connection to earth/ground is available through water on the floor or a water faucet. With the earth/ground connection intact, the circuit breaker will trip, forcing repair of the appliance. Why are some appliances still sold with two-prong plugs? These have nonconducting cases, such as power tools with impact resistant plastic cases, and are called doubly insulated. Modern two-prong plugs can be inserted into the asymmetric standard outlet in only one way, to ensure proper connection of live/hot and neutral wires.

  
FIGURE 23.32 Worn insulation allows the live/hot wire to come into direct contact with the metal case of this appliance. (a) The earth/ ground connection being broken, the person is severely shocked. The appliance may operate normally in this situation. (b) With a proper earth/ground, the circuit breaker trips, forcing repair of the appliance.

Electromagnetic induction causes a more subtle problem that is solved by grounding the case. The AC current in appliances can induce an emf on the case. If grounded, the case voltage is kept near zero, but if the case is not grounded, a shock can occur as pictured in Figure 23.33. Current driven by the induced case emf is called a leakagecurrent, although current does not necessarily pass from the resistor to the case.

  
FIGURE 23.33 AC currents can induce an emf on the case of an appliance. The voltage can be large enough to cause a shock. If the case is grounded, the induced emf is kept near zero.

A ground fault interrupter (GFI) is a safety device found in updated kitchen and bathroom wiring that works based on electromagnetic induction. GFIs compare the currents in the live/hot and neutral wires. When live/hot and neutral currents are not equal, it is almost always because current in the neutral is less than in the live/hot wire. Then some of the current, again called a leakage current, is returning to the voltage source by a path other than through the neutral wire. It is assumed that this path presents a hazard, such as shown in Figure 23.34. GFIs are usually set to interrupt the circuit if the leakage current is greater than  , the accepted maximum harmless shock. Even if the leakage current goes safely to earth/ground through an intact earth/ground wire, the GFI will trip, forcing repair of the leakage.

  
FIGURE 23.34 A ground fault interrupter (GFI) compares the currents in the live/hot and neutral wires and will trip if their difference exceeds a safe value. The leakage current here follows a hazardous path that could have been prevented by an intact earth/ground wire

Figure 23.35 shows how a GFI works. If the currents in the live/hot and neutral wires are equal, then they induce equal and opposite emfs in the coil. If not, then the circuit breaker will trip.  
FIGURE 23.35 A GFI compares currents by using both to induce an emf in the same coil. If the currents are equal, they will induce equal but opposite emfs.

Another induction-based safety device is the isolation transformer, shown in Figure 23.36. Most isolation transformers have equal input and output voltages. Their function is to put a large resistance between the original voltage source and the device being operated. This prevents a complete circuit between them, even in the circumstance shown. There is a complete circuit through the appliance. But there is not a complete circuit for current to flow through the person in the figure, who is touching only one of the transformer’s output wires, and neither output wire is grounded. The appliance is isolated from the original voltage source by the high resistance of the material between the transformer coils, hence the name isolation transformer. For current to flow through the person, it must pass through the high-resistance material between the coils, through the wire, the person, and back through the earth—a path with such a large resistance that the current is negligible.

  
FIGURE 23.36 An isolation transformer puts a large resistance between the original voltage source and the device, preventing a complete circuit between them.

The basics of electrical safety presented here help prevent many electrical hazards. Electrical safety can be pursued to greater depths. There are, for example, problems related to different earth/ground connections for appliances in close proximity. Many other examples are found in hospitals. Microshock-sensitive patients, for instance, require special protection. For these people, currents as low as  may cause ventricular fibrillation. The interested reader can use the material presented here as a basis for further study.

# 23.9 Inductance

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Calculate the inductance of an inductor.   
Calculate the energy stored in an inductor.   
Calculate the emf generated in an inductor.

# Inductors

Induction is the process in which an emf is induced by changing magnetic flux. Many examples have been discussed so far, some more effective than others. Transformers, for example, are designed to be particularly effective atinducing a desired voltage and current with very little loss of energy to other forms. Is there a useful physical quantity related to how “effective” a given device is? The answer is yes, and that physical quantity is called inductance.

Mutual inductance is the effect of Faraday’s law of induction for one device upon another, such as the primary coil in transmitting energy to the secondary in a transformer. See Figure 23.37, where simple coils induce emfs in one another.

  
FIGURE 23.37 These coils can induce emfs in one another like an inefficient transformer. Their mutual inductance M indicates the effectiveness of the coupling between them. Here a change in current in coil 1 is seen to induce an emf in coil 2. (Note that "  induced" represents the induced emf in coil 2.)

In the many cases where the geometry of the devices is fixed, flux is changed by varying current. We therefore concentrate on the rate of change of current,  , as the cause of induction. A change in the current  in one device, coil 1 in the figure, induces an  in the other. We express this in equation form as



where  is defined to be the mutual inductance between the two devices. The minus sign is an expression of Lenz’s law. The larger the mutual inductance  , the more effective the coupling. For example, the coils in Figure 23.37 have a small  compared with the transformer coils in Figure 23.27. Units for  are  , which is named a henry (H), after Joseph Henry. That is,  .

Nature is symmetric here. If we change the current  in coil 2, we induce an  in coil 1, which is given by



where  is the same as for the reverse process. Transformers run backward with the same effectiveness, or mutual inductance  .

A large mutual inductance  may or may not be desirable. We want a transformer to have a large mutual inductance. But an appliance, such as an electric clothes dryer, can induce a dangerous emf on its case if the mutual inductance between its coils and the case is large. One way to reduce mutual inductance  is to counterwind coils to cancel the magnetic field produced. (See Figure 23.38.)  
FIGURE 23.38 The heating coils of an electric clothes dryer can be counter-wound so that their magnetic fields cancel one another, greatly reducing the mutual inductance with the case of the dryer.

Self-inductance, the effect of Faraday’s law of induction of a device on itself, also exists. When, for example, current through a coil is increased, the magnetic field and flux also increase, inducing a counter emf, as required by Lenz’s law. Conversely, if the current is decreased, an emf is induced that opposes the decrease. Most devices have a fixed geometry, and so the change in flux is due entirely to the change in current  through the device. The induced emf is related to the physical geometry of the device and the rate of change of current. It is given by



where  is the self-inductance of the device. A device that exhibits significant self-inductance is called an inductor, and given the symbol in Figure 23.39.

  
FIGURE 23.39

The minus sign is an expression of Lenz’s law, indicating that emf opposes the change in current. Units of selfinductance are henries (H) just as for mutual inductance. The larger the self-inductance  of a device, the greater its opposition to any change in current through it. For example, a large coil with many turns and an iron core has a large  and will not allow current to change quickly. To avoid this effect, a small  must be achieved, such as by counterwinding coils as in Figure 23.38.

A 1 H inductor is a large inductor. To illustrate this, consider a device with  that has a 10 A current flowing through it. What happens if we try to shut off the current rapidly, perhaps in only  An emf, given by  , will oppose the change. Thus an emf will be induced given by   
 The positive sign means this large voltage is in the same direction as the current, opposing its decrease. Such large emfs can cause arcs, damaging switching equipment, and so it may be necessary to change current more slowly.

There are uses for such a large induced voltage. Camera flashes use a battery, two inductors that function as a transformer, and a switching system or oscillator to induce large voltages. (Remember that we need a changing magnetic field, brought about by a changing current, to induce a voltage in another coil.) The oscillator system will do this many times as the battery voltage is boosted to over one thousand volts. (You may hear the high pitched whine from the transformer as the capacitor is being charged.) A capacitor stores the high voltage for later use in powering the flash. (See Figure 23.40.)  
FIGURE 23.40 Through rapid switching of an inductor,  batteries can be used to induce emfs of several thousand volts. This voltage can be used to store charge in a capacitor for later use, such as in a camera flash attachment.

It is possible to calculate  for an inductor given its geometry (size and shape) and knowing the magnetic field that it produces. This is difficult in most cases, because of the complexity of the field created. So in this text the inductance  is usually a given quantity. One exception is the solenoid, because it has a very uniform field inside, a nearly zero field outside, and a simple shape. It is instructive to derive an equation for its inductance. We start by noting that the induced emf is given by Faraday’s law of induction as  and, by the definition of self-inductance, as  . Equating these yields



Solving for  gives



This equation for the self-inductance  of a device is always valid. It means that self-inductance  depends on how effective the current is in creating flux; the more effective, the greater  is.

Let us use this last equation to find an expression for the inductance of a solenoid. Since the area  of a solenoid is fixed, the change in flux is  To find  , we note that the magnetic field of a solenoid is given by  . (Here , where is the number of coils and is the solenoid’s length.) Only the current changes, so that  . Substituting  into  gives



This simplifies to



This is the self-inductance of a solenoid of cross-sectional area  and length  . Note that the inductance depends only on the physical characteristics of the solenoid, consistent with its definition.

# EXAMPLE 23.7

# Calculating the Self-inductance of a Moderate Size Solenoid

Calculate the self-inductance of a  long,  diameter solenoid that has 200 coils.

# Strategy

This is a straightforward application of  , since all quantities in the equation except  are known.

# Solution

Use the following expression for the self-inductance of a solenoid:

The cross-sectional area in this example is  ,  is given to be 200, and the length  is  . We know the permeability of free space is  . Substituting these into the expression for  gives



# Discussion

This solenoid is moderate in size. Its inductance of nearly a millihenry is also considered moderate.

One common application of inductance is used in traffic lights that can tell when vehicles are waiting at the intersection. An electrical circuit with an inductor is placed in the road under the place a waiting car will stop over. The body of the car increases the inductance and the circuit changes sending a signal to the traffic lights to change colors. Similarly, metal detectors used for airport security employ the same technique. A coil or inductor in the metal detector frame acts as both a transmitter and a receiver. The pulsed signal in the transmitter coil induces a signal in the receiver. The self-inductance of the circuit is affected by any metal object in the path. Such detectors can be adjusted for sensitivity and also can indicate the approximate location of metal found on a person. See Figure 23.41.

  
FIGURE 23.41 The familiar security gate at an airport can not only detect metals but also indicate their approximate height above the floor. (credit: shankar s/Flickr)

# Energy Stored in an Inductor

We know from Lenz’s law that inductances oppose changes in current. There is an alternative way to look at this opposition that is based on energy. Energy is stored in a magnetic field. It takes time to build up energy, and it also takes time to deplete energy; hence, there is an opposition to rapid change. In an inductor, the magnetic field is directly proportional to current and to the inductance of the device. It can be shown that the energy stored in an inductor  is given by



This expression is similar to that for the energy stored in a capacitor.

# EXAMPLE 23.8

# Calculating the Energy Stored in the Field of a Solenoid

How much energy is stored in the  inductor of the preceding example when a 30.0 A current flows through it?# Strategy

The energy is given by the equation  , and all quantities except  are known.

# Solution

Substituting the value for  found in the previous example and the given current into  gives



# Discussion

This amount of energy is certainly enough to cause a spark if the current is suddenly switched off. It cannot be built up instantaneously unless the power input is infinite.

# 23.10 RL Circuits

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Calculate the current in an RL circuit after a specified number of characteristic time steps.   
Calculate the characteristic time of an RL circuit.   
Sketch the current in an RL circuit over time.

We know that the current through an inductor  cannot be turned on or off instantaneously. The change in current changes flux, inducing an emf opposing the change (Lenz’s law). How long does the opposition last? Current will flow and can be turned off, but how long does it take? Figure 23.42 shows a switching circuit that can be used to examine current through an inductor as a function of time.

  
FIGURE 23.42 (a) An RL circuit with a switch to turn current on and off. When in position 1, the battery, resistor, and inductor are in series and a current is established. In position 2, the battery is removed and the current eventually stops because of energy loss in the resistor. (b) A graph of current growth versus time when the switch is moved to position 1. (c) A graph of current decay when the switch is moved to position 2.

When the switch is first moved to position 1 (at  ), the current is zero and it eventually rises to  , where  is the total resistance of the circuit. The opposition of the inductor  is greatest at the beginning, because the amount of change is greatest. The opposition it poses is in the form of an induced emf, which decreases to zero as the current approaches its final value. The opposing emf is proportional to the amount of change left. This is the hallmark of an exponential behavior, and it can be shown with calculus that



is the current in an  circuit when switched on (Note the similarity to the exponential behavior of the voltage on a charging capacitor). The initial current is zero and approaches  with a characteristic time constant  for an  circuit, given by

where  has units of seconds, since  . In the first period of time  , the current rises from zero to  , since  . The current will  of the remainder in the next time  . A well-known property of the exponential is that the final value is never exactly reached, but 0.632 of the remainder to that value is achieved in every characteristic time  . In just a few multiples of the time  , the final value is very nearly achieved, as the graph in Figure 23.42(b) illustrates.

The characteristic time  depends on only two factors, the inductance  and the resistance  . The greater the inductance  , the greater  is, which makes sense since a large inductance is very effective in opposing change. The smaller the resistance  , the greater  is. Again this makes sense, since a small resistance means a large final current and a greater change to get there. In both cases—large  and small  —more energy is stored in the inductor and more time is required to get it in and out.

When the switch in Figure 23.42(a) is moved to position 2 and cuts the battery out of the circuit, the current drops because of energy dissipation by the resistor. But this is also not instantaneous, since the inductor opposes the decrease in current by inducing an emf in the same direction as the battery that drove the current. Furthermore, there is a certain amount of energy,  , stored in the inductor, and it is dissipated at a finite rate. As the current approaches zero, the rate of decrease slows, since the energy dissipation rate is  . Once again the behavior is exponential, and  is found to be



(See Figure 23.42(c).) In the first period of time  after the switch is closed, the current falls to 0.368 of its initial value, since  . In each successive time  , the current falls to 0.368 of the preceding value, and in a few multiples of  , the current becomes very close to zero, as seen in the graph in Figure 23.42(c).

# EXAMPLE 23.9

# Calculating Characteristic Time and Current in an RL Circuit

(a) What is the characteristic time constant for a  inductor in series with a  resistor? (b) Find the current  after the switch is moved to position 2 to disconnect the battery, if it is initially  .

# Strategy for (a)

The time constant for an  circuit is defined by  .

# Solution for (a)

Entering known values into the expression for  given in  yields



# Discussion for (a)

This is a small but definitely finite time. The coil will be very close to its full current in about ten time constants, or about  .

# Strategy for (b)

We can find the current by using  , or by considering the decline in steps. Since the time is twice the characteristic time, we consider the process in steps.

# Solution for (b)

In the first  , the current declines to 0.368 of its initial value, which is



After another 2.50 ms, or a total of  , the current declines to 0.368 of the value just found. That is,

# Discussion for (b)

After another 5.00 ms has passed, the current will be 0.183 A (see Exercise 23.69); so, although it does die out, the current certainly does not go to zero instantaneously.

In summary, when the voltage applied to an inductor is changed, the current also changes, but the change in current .p behaves when a sinusoidal AC voltage is applied.

# 23.11 Reactance, Inductive and Capacitive

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Sketch voltage and current versus time in simple inductive, capacitive, and resistive circuits.   
Calculate inductive and capacitive reactance.   
Calculate current and/or voltage in simple inductive, capacitive, and resistive circuits.

Many circuits also contain capacitors and inductors, in addition to resistors and an AC voltage source. We have seen how capacitors and inductors respond to DC voltage when it is switched on and off. We will now explore how inductors and capacitors react to sinusoidal AC voltage.

# Inductors and Inductive Reactance

Suppose an inductor is connected directly to an AC voltage source, as shown in Figure 23.43. It is reasonable to assume negligible resistance, since in practice we can make the resistance of an inductor so small that it has a negligible effect on the circuit. Also shown is a graph of voltage and current as functions of time.

  
FIGURE 23.43 (a) An AC voltage source in series with an inductor having negligible resistance. (b) Graph of current and voltage across the inductor as functions of time.

The graph in Figure 23.43(b) starts with voltage at a maximum. Note that the current starts at zero and rises to its peak after the voltage that drives it, just as was the case when DC voltage was switched on in the preceding section. When the voltage becomes negative at point a, the current begins to decrease; it becomes zero at point b, where voltage is its most negative. The current then becomes negative, again following the voltage. The voltage becomes positive at point c and begins to make the current less negative. At point d, the current goes through zero just as the voltage reaches its positive peak to start another cycle. This behavior is summarized as follows:

# AC Voltage in an Inductor

When a sinusoidal voltage is applied to an inductor, the voltage leads the current by one-fourth of a cycle, or by a  phase angle.

Current lags behind voltage, since inductors oppose change in current. Changing current induces a back emf  . This is considered to be an effective resistance of the inductor to AC. The rms current  throughan inductor  is given by a version of Ohm’s law:



where  is the rms voltage across the inductor and  is defined to be



with  the frequency of the AC voltage source in hertz (An analysis of the circuit using Kirchhoff’s loop rule and calculus actually produces this expression).  is called the inductive reactance, because the inductor reacts to impede the current.  has units of ohms (  , so that frequency times inductance has units of (cycles/s)  , consistent with its role as an effective resistance. It makes sense that  is proportional to  , since the greater the induction the greater its resistance to change. It is also reasonable that  is proportional to frequency  , since greater frequency means greater change in current. That is,  is large for large frequencies (large  , small  ). The greater the change, the greater the opposition of an inductor.

# EXAMPLE 23.10

# Calculating Inductive Reactance and then Current

(a) Calculate the inductive reactance of a  inductor when  and  AC voltages are applied. (b) What is the rms current at each frequency if the applied rms voltage is 120 V?

# Strategy

The inductive reactance is found directly from the expression  . Once  has been found at each frequency, Ohm’s law as stated in the Equation  can be used to find the current at each frequency.

# Solution for (a)

Entering the frequency and inductance into Equation  gives



Similarly, at  ,



# Solution for (b)

The rms current is now found using the version of Ohm’s law in Equation  , given the applied rms voltage is  For the first frequency, this yields



Similarly, at 



# Discussion

The inductor reacts very differently at the two different frequencies. At the higher frequency, its reactance is large and the current is small, consistent with how an inductor impedes rapid change. Thus high frequencies are impeded the most. Inductors can be used to filter out high frequencies; for example, a large inductor can be put in series with a sound reproduction system or in series with your home computer to reduce high-frequency sound output from your speakers or high-frequency power spikes into your computer.

Note that although the resistance in the circuit considered is negligible, the AC current is not extremely large because inductive reactance impedes its flow. With AC, there is no time for the current to become extremely large.# Capacitors and Capacitive Reactance

Consider the capacitor connected directly to an AC voltage source as shown in Figure 23.44. The resistance of a circuit like this can be made so small that it has a negligible effect compared with the capacitor, and so we can assume negligible resistance. Voltage across the capacitor and current are graphed as functions of time in the figure.

  
FIGURE 23.44 (a) An AC voltage source in series with a capacitor C having negligible resistance. (b) Graph of current and voltage across the capacitor as functions of time.

The graph in Figure 23.44 starts with voltage across the capacitor at a maximum. The current is zero at this point, because the capacitor is fully charged and halts the flow. Then voltage drops and the current becomes negative as the capacitor discharges. At point a, the capacitor has fully discharged  on it) and the voltage across it is zero. The current remains negative between points a and b, causing the voltage on the capacitor to reverse. This is complete at point b, where the current is zero and the voltage has its most negative value. The current becomes positive after point b, neutralizing the charge on the capacitor and bringing the voltage to zero at point c, which allows the current to reach its maximum. Between points c and d, the current drops to zero as the voltage rises to its peak, and the process starts to repeat. Throughout the cycle, the voltage follows what the current is doing by onefourth of a cycle:

# AC Voltage in a Capacitor

When a sinusoidal voltage is applied to a capacitor, the voltage follows the current by one-fourth of a cycle, or by a  phase angle.

The capacitor is affecting the current, having the ability to stop it altogether when fully charged. Since an AC voltage is applied, there is an rms current, but it is limited by the capacitor. This is considered to be an effective resistance of the capacitor to AC, and so the rms current  in the circuit containing only a capacitor  is given by another version of Ohm’s law to be



where  is the rms voltage and  is defined (As with  , this expression for  results from an analysis of the circuit using Kirchhoff’s rules and calculus) to be



where  is called the capacitive reactance, because the capacitor reacts to impede the current.  has units of ohms (verification left as an exercise for the reader).  is inversely proportional to the capacitance  ; the larger the capacitor, the greater the charge it can store and the greater the current that can flow. It is also inversely proportional to the frequency  ; the greater the frequency, the less time there is to fully charge the capacitor, and so it impedes current less.# EXAMPLE 23.11

# Calculating Capacitive Reactance and then Current

(a) Calculate the capacitive reactance of a  capacitor when  and 10.0 kHz AC voltages are applied. (b) What is the rms current if the applied rms voltage is 120 V?

# Strategy

The capacitive reactance is found directly from the expression in  . Once  has been found at each frequency, Ohm’s law stated as  can be used to find the current at each frequency.

# Solution for (a)

Entering the frequency and capacitance into  gives



Similarly, at 



# Solution for (b)

The rms current is now found using the version of Ohm’s law in  , given the applied rms voltage is  . For the first frequency, this yields



Similarly, at  ,



# Discussion

The capacitor reacts very differently at the two different frequencies, and in exactly the opposite way an inductor reacts. At the higher frequency, its reactance is small and the current is large. Capacitors favor change, whereas inductors oppose change. Capacitors impede low frequencies the most, since low frequency allows them time to become charged and stop the current. Capacitors can be used to filter out low frequencies. For example, a capacitor in series with a sound reproduction system rids it of the  hum.

Although a capacitor is basically an open circuit, there is an rms current in a circuit with an AC voltage applied to a capacitor. This is because the voltage is continually reversing, charging and discharging the capacitor. If the frequency goes to zero (DC),  tends to infinity, and the current is zero once the capacitor is charged. At very high frequencies, the capacitor’s reactance tends to zero—it has a negligible reactance and does not impede the current (it acts like a simple wire). Capacitors have the opposite effect on AC circuits that inductors have.

# Resistors in an AC Circuit

Just as a reminder, consider Figure 23.45, which shows an AC voltage applied to a resistor and a graph of voltage and current versus time. The voltage and current are exactly in phase in a resistor. There is no frequency dependence to the behavior of plain resistance in a circuit:  
FIGURE 23.45 (a) An AC voltage source in series with a resistor. (b) Graph of current and voltage across the resistor as functions of time, showing them to be exactly in phase.

# AC Voltage in a Resistor

When a sinusoidal voltage is applied to a resistor, the voltage is exactly in phase with the current—they have a  phase angle.

# 23.12 RLC Series AC Circuits

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Calculate the impedance, phase angle, resonant frequency, power, power factor, voltage, and/or current in a RLC series circuit.   
Draw the circuit diagram for an RLC series circuit.   
Explain the significance of the resonant frequency.

# Impedance

When alone in an AC circuit, inductors, capacitors, and resistors all impede current. How do they behave when all three occur together? Interestingly, their individual resistances in ohms do not simply add. Because inductors and capacitors behave in opposite ways, they partially to totally cancel each other’s effect. Figure 23.46 shows an RLC series circuit with an AC voltage source, the behavior of which is the subject of this section. The crux of the analysis of an RLC circuit is the frequency dependence of  and  , and the effect they have on the phase of voltage versus current (established in the preceding section). These give rise to the frequency dependence of the circuit, with important “resonance” features that are the basis of many applications, such as radio tuners.

  
FIGURE 23.46 An RLC series circuit with an AC voltage source.

The combined effect of resistance  , inductive reactance  , and capacitive reactance  is defined to be impedance, an AC analogue to resistance in a DC circuit. Current, voltage, and impedance in an  circuit are related by an AC version of Ohm’s law:

Here  is the peak current,  the peak source voltage, and  is the impedance of the circuit. The units of impedance are ohms, and its effect on the circuit is as you might expect: the greater the impedance, the smaller the current. To get an expression for  in terms of  ,  , and  , we will now examine how the voltages across the various components are related to the source voltage. Those voltages are labeled  , and  in Figure 23.46.

Conservation of charge requires current to be the same in each part of the circuit at all times, so that we can say the currents in  , and  are equal and in phase. But we know from the preceding section that the voltage across the inductor  leads the current by one-fourth of a cycle, the voltage across the capacitor  follows the current by one-fourth of a cycle, and the voltage across the resistor  is exactly in phase with the current. Figure 23.47 shows these relationships in one graph, as well as showing the total voltage around the circuit  , where all four voltages are the instantaneous values. According to Kirchhoff’s loop rule, the total voltage around the circuit  is also the voltage of the source.

You can see from Figure 23.47 that while  is in phase with the current,  leads by  , and  follows by  . Thus  and  are  out of phase (crest to trough) and tend to cancel, although not completely unless they have the same magnitude. Since the peak voltages are not aligned (not in phase), the peak voltage  of the source does not equal the sum of the peak voltages across  , and  . The actual relationship is



where  , and  are the peak voltages across  , and  , respectively. Now, using Ohm’s law and definitions from Reactance, Inductive and Capacitive, we substitute  into the above, as well as  , and  , yielding



 cancels to yield an expression for  :



which is the impedance of an  series AC circuit. For circuits without a resistor, take  ; for those without an inductor, take  ; and for those without a capacitor, take  .

  
FIGURE 23.47 This graph shows the relationships of the voltages in an RLC circuit to the current. The voltages across the circuit elements add to equal the voltage of the source, which is seen to be out of phase with the current.# EXAMPLE 23.12

# Calculating Impedance and Current

An RLC series circuit has a  resistor, a  inductor, and a  capacitor. (a) Find the circuit’s impedance at  and  , noting that these frequencies and the values for  and  are the same as in Example 23.10 and Example 23.11. (b) If the voltage source has  , what is  at each frequency?

# Strategy

For each frequency, we use  to find the impedance and then Ohm’s law to find current. We can take advantage of the results of the previous two examples rather than calculate the reactances again.

# Solution for (a)

At  , the values of the reactances were found in Example 23.10 to be  and in Example 23.11 to be  . Entering these and the given  for resistance into  yields



Similarly, at  ,  and  , so that



# Discussion for (a)

In both cases, the result is nearly the same as the largest value, and the impedance is definitely not the sum of the individual values. It is clear that  dominates at high frequency and  dominates at low frequency.

# Solution for (b)

The current  can be found using the AC version of Ohm’s law in Equation  :



Finally, at  , we find



# Discussion for (a)

The current at  is the same (to three digits) as found for the capacitor alone in Example 23.11. The capacitor dominates at low frequency. The current at  is only slightly different from that found for the inductor alone in Example 23.10. The inductor dominates at high frequency.

# Resonance in RLC Series AC Circuits

How does an  circuit behave as a function of the frequency of the driving voltage source? Combining Ohm’s law,  , and the expression for impedance  from  gives



The reactances vary with frequency, with  large at high frequencies and  large at low frequencies, as we have seen in three previous examples. At some intermediate frequency  , the reactances will be equal and cancel, giving  —this is a minimum value for impedance, and a maximum value for  results. We can get anexpression for  by taking



Substituting the definitions of  and  ,



Solving this expression for  yields



where  is the resonant frequency of an RLC series circuit. This is also the natural frequency at which the circuit would oscillate if not driven by the voltage source. At  , the effects of the inductor and capacitor cancel, so that  , and  is a maximum.

Resonance in AC circuits is analogous to mechanical resonance, where resonance is defined to be a forced oscillation—in this case, forced by the voltage source—at the natural frequency of the system. The receiver in a radio is an  circuit that oscillates best at its  . A variable capacitor is often used to adjust  to receive a desired frequency and to reject others. Figure 23.48 is a graph of current as a function of frequency, illustrating a resonant peak in  at  . The two curves are for two different circuits, which differ only in the amount of resistance in them. The peak is lower and broader for the higher-resistance circuit. Thus the higher-resistance circuit does not resonate as strongly and would not be as selective in a radio receiver, for example.

  
FIGURE 23.48 A graph of current versus frequency for two RLC series circuits differing only in the amount of resistance. Both have a resonance at  , but that for the higher resistance is lower and broader. The driving AC voltage source has a fixed amplitude  .

# EXAMPLE 23.13

# Calculating Resonant Frequency and Current

For the same RLC series circuit having a  resistor, a  inductor, and a  capacitor: (a) Find the resonant frequency. (b) Calculate  at resonance if  is  .

# Strategy

The resonant frequency is found by using the expression in  . The current at that frequency is the same as if the resistor alone were in the circuit.

# Solution for (a)

Entering the given values for  and  into the expression given for  in  yields

# Discussion for (a)

We see that the resonant frequency is between  and  , the two frequencies chosen in earlier examples. This was to be expected, since the capacitor dominated at the low frequency and the inductor dominated at the high frequency. Their effects are the same at this intermediate frequency.

# Solution for (b)

The current is given by Ohm’s law. At resonance, the two reactances are equal and cancel, so that the impedance equals the resistance alone. Thus,



# Discussion for (b)

At resonance, the current is greater than at the higher and lower frequencies considered for the same circuit in the preceding example.

# Power in RLC Series AC Circuits

If current varies with frequency in an RLC circuit, then the power delivered to it also varies with frequency. But the average power is not simply current times voltage, as it is in purely resistive circuits. As was seen in Figure 23.47, voltage and current are out of phase in an RLC circuit. There is a phase angle  between the source voltage  and the current  , which can be found from



For example, at the resonant frequency or in a purely resistive circuit  , so that  . This implies that  and that voltage and current are in phase, as expected for resistors. At other frequencies, average power is less than at resonance. This is both because voltage and current are out of phase and because  is lower. The fact that source voltage and current are out of phase affects the power delivered to the circuit. It can be shown that the average power is



Thus  is called the power factor, which can range from 0 to 1. Power factors near 1 are desirable when designing an efficient motor, for example. At the resonant frequency,  .

# EXAMPLE 23.14

# Calculating the Power Factor and Power

For the same  series circuit having a  resistor, a  inductor, a  capacitor, and a voltage source with a  of  : (a) Calculate the power factor and phase angle for  . (b) What is the average power at  (c) Find the average power at the circuit’s resonant frequency.

# Strategy and Solution for (a)

The power factor at  is found from



We know  from Example 23.12, so that



This small value indicates the voltage and current are significantly out of phase. In fact, the phase angle is# Discussion for (a)

The phase angle is close to  , consistent with the fact that the capacitor dominates the circuit at this low frequency (a pure RC circuit has its voltage and current  out of phase).

# Strategy and Solution for (b)

The average power at  is



 was found to be 0.226 A in Example 23.12. Entering the known values gives



# Strategy and Solution for (c)

At the resonant frequency, we know  , and  was found to be 6.00 A in Example 23.13. Thus,

 at resonance 

# Discussion

Both the current and the power factor are greater at resonance, producing significantly greater power than at higher and lower frequencies.

Power delivered to an RLC series AC circuit is dissipated by the resistance alone. The inductor and capacitor have energy input and output but do not dissipate it out of the circuit. Rather they transfer energy back and forth to one another, with the resistor dissipating exactly what the voltage source puts into the circuit. This assumes no significant electromagnetic radiation from the inductor and capacitor, such as radio waves. Such radiation can happen and may even be desired, as we will see in the next chapter on electromagnetic radiation, but it can also be suppressed as is the case in this chapter. The circuit is analogous to the wheel of a car driven over a corrugated road as shown in Figure 23.49. The regularly spaced bumps in the road are analogous to the voltage source, driving the wheel up and down. The shock absorber is analogous to the resistance damping and limiting the amplitude of the oscillation. Energy within the system goes back and forth between kinetic (analogous to maximum current, and energy stored in an inductor) and potential energy stored in the car spring (analogous to no current, and energy stored in the electric field of a capacitor). The amplitude of the wheels’ motion is a maximum if the bumps in the road are hit at the resonant frequency.

  
FIGURE 23.49 The forced but damped motion of the wheel on the car spring is analogous to an RLC series AC circuit. The shock absorber damps the motion and dissipates energy, analogous to the resistance in an  circuit. The mass and spring determine the resonant frequency.

A pure LC circuit with negligible resistance oscillates at  , the same resonant frequency as an RLC circuit. It can serve as a frequency standard or clock circuit—for example, in a digital wristwatch. With a very small resistance, only a very small energy input is necessary to maintain the oscillations. The circuit is analogous to a car with no shock absorbers. Once it starts oscillating, it continues at its natural frequency for some time. Figure 23.50 shows theanalogy between an LC circuit and a mass on a spring.

  
FIGURE 23.50 An LC circuit is analogous to a mass oscillating on a spring with no friction and no driving force. Energy moves back and forth between the inductor and capacitor, just as it moves from kinetic to potential in the mass-spring system.

# PHET EXPLORATIONS

# Circuit Construction Kit  , Virtual Lab

Build circuits with capacitors, inductors, resistors and AC or DC voltage sources, and inspect them using lab instruments such as voltmeters and ammeters.

Click to view content (https://openstax.org/books/college-physics-2e/pages/23-12-rlc-series-ac-circuits)# Glossary

back emf the emf generated by a running motor, because it consists of a coil turning in a magnetic field; it opposes the voltage powering the motor   
capacitive reactance the opposition of a capacitor to a change in current; calculated by   
characteristic time constant denoted by  , of a particular series  circuit is calculated by  , where  is the inductance and  is the resistance   
eddy current a current loop in a conductor caused by motional emf   
electric generator a device for converting mechanical work into electric energy; it induces an emf by rotating a coil in a magnetic field   
electromagnetic induction the process of inducing an emf (voltage) with a change in magnetic flux   
emf induced in a generator coil  sin  , where  is the area of an  -turn coil rotated at a constant angular velocity  in a uniform magnetic field  , over a period of time    
energy stored in an inductor self-explanatory; calculated by    
Faraday’s law of induction the means of calculating the emf in a coil due to changing magnetic flux, given by   
henry the unit of inductance;    
impedance the AC analogue to resistance in a DC circuit; it is the combined effect of resistance, inductive reactance, and capacitive reactance in the form    
inductance a property of a device describing how efficient it is at inducing emf in another device   
induction (magnetic induction) the creation of emfs and hence currents by magnetic fields   
inductive reactance the opposition of an inductor to a change in current; calculated by    
inductor a device that exhibits significant selfinductance   
Lenz’s law the minus sign in Faraday’s law, signifying that the emf induced in a coil opposes the change in magnetic flux   
magnetic damping the drag produced by eddy currents   
magnetic flux the amount of magnetic field going through a particular area, calculated with  cos  where  is the magnetic field strength over an area  at an angle  with the perpendicular to the area   
mutual inductance how effective a pair of devices are at inducing emfs in each other   
peak emf    
phase angle denoted by  , the amount by which the voltage and current are out of phase with each other in a circuit   
power factor the amount by which the power delivered in the circuit is less than the theoretical maximum of the circuit due to voltage and current being out of phase; calculated by    
resonant frequency the frequency at which the impedance in a circuit is at a minimum, and also the frequency at which the circuit would oscillate if not driven by a voltage source; calculated by    
self-inductance how effective a device is at inducing emf in itself   
shock hazard the term for electrical hazards due to current passing through a human   
step-down transformer a transformer that decreases voltage   
step-up transformer a transformer that increases voltage   
thermal hazard the term for electrical hazards due to overheating   
three-wire system the wiring system used at present for safety reasons, with live, neutral, and ground wires   
transformer a device that transforms voltages from one value to another using induction   
transformer equation the equation showing that the ratio of the secondary to primary voltages in a transformer equals the ratio of the number of loops in their coils; 

# Section Summary

# 23.1 Induced Emf and Magnetic Flux

• The crucial quantity in induction is magnetic flux  , defined to be  cos  , where  is the magnetic field strength over an area  at an angle  with the perpendicular to the area. • Units of magnetic flux  are  . • Any change in magnetic flux  induces an

emf—the process is defined to be electromagnetic induction.

# 23.2 Faraday’s Law of Induction: Lenz’s Law

• Faraday’s law of induction states that the emfinduced by a change in magnetic flux is   
when flux changes by  in a time  .   
• If emf is induced in a coil,  is its number of turns. The minus sign means that the emf creates a   
current  and magnetic field  that oppose the change in flux  —this opposition is known as Lenz’s law.

# 23.3 Motional Emf

• An emf induced by motion relative to a magnetic field  is called a motional emf and is given by   , and  perpendicular), where  is the length of the object moving at speed  relative to the field.

# 23.4 Eddy Currents and Magnetic Damping

• Current loops induced in moving conductors are called eddy currents.   
• They can create significant drag, called magnetic damping.

# 23.5 Electric Generators

• An electric generator rotates a coil in a magnetic field, inducing an emfgiven as a function of time by  sin  , where  is the area of an  -turn coil rotated at a constant angular velocity  in a uniform magnetic field  .   
The peak emf  of a generator is 

# 23.6 Back Emf

• Any rotating coil will have an induced emf—in motors, this is called back emf, since it opposes the emf input to the motor.

# 23.7 Transformers

• Transformers use induction to transform voltages from one value to another. For a transformer, the voltages across the primary and secondary coils are related by  where  and  are the voltages across primary and secondary coils having  and  turns.   
• The currents  and  in the primary and secondary coils are related by  . A step-up transformer increases voltage and decreases current, whereas a step-down transformer decreases voltage and increases current.   
• Electrical safety systems and devices are employed to prevent thermal and shock hazards. Circuit breakers and fuses interrupt excessive currents to prevent thermal hazards. The three-wire system guards against thermal and shock hazards, utilizing live/hot, neutral, and earth/ground wires, and grounding the neutral wire and case of the appliance. A ground fault interrupter (GFI) prevents shock by detecting the loss of current to unintentional paths. An isolation transformer insulates the device being powered from the original source, also to prevent shock.   
• Many of these devices use induction to perform their basic function.

# 23.9 Inductance

• Inductance is the property of a device that tells how effectively it induces an emf in another device. Mutual inductance is the effect of two devices in inducing emfs in each other.   
• A change in current  in one induces an emf  in the second:  where  is defined to be the mutual inductance between the two devices, and the minus sign is due to Lenz’s law. Symmetrically, a change in current  through the second device induces an emf in the first:  where  is the same mutual inductance as in the reverse process. Current changes in a device induce an emf in the device itself. Self-inductance is the effect of the device inducing emf in itself. The device is called an inductor, and the emf induced in it by a change in current through it is  where  is the self-inductance of the inductor, and  is the rate of change of current through it. The minus sign indicates that emf opposes the change in current, as required by Lenz’s law. The unit of self- and mutual inductance is the henry (H), where  .   
• The self-inductance  of an inductor isproportional to how much flux changes with current. For an  -turn inductor,    
The self-inductance of a solenoid is  where  is its number of turns in the solenoid, is its cross-sectional area,  is its length, and  is the permeability of free space.   
• The energy stored in an inductor  is 

# 23.10 RL Circuits

• When a series connection of a resistor and an inductor—an  circuit—is connected to a voltage source, the time variation of the current is  (turning on). where  is the final current.   
• The characteristic time constant is , where  is the inductance and  is the resistance. In the first time constant  , the current rises from zero to  , and 0.632 of the remainder in every subsequent time interval  . When the inductor is shorted through a resistor, current decreases as  (turning off). Here  is the initial current. Current falls to  in the first time interval  , and 0.368 of the remainder toward zero in each subsequent time  .

# 23.11 Reactance, Inductive and Capacitive

• For inductors in AC circuits, we find that when a sinusoidal voltage is applied to an inductor, the voltage leads the current by one-fourth of a cycle, or by a  phase angle. The opposition of an inductor to a change in current is expressed as a type of AC resistance. Ohm’s law for an inductor is  where  is the rms voltage across the inductor.  is defined to be the inductive reactance, given by 

with  the frequency of the AC voltage source in hertz.   
Inductive reactance  has units of ohms and is greatest at high frequencies.   
For capacitors, we find that when a sinusoidal voltage is applied to a capacitor, the voltage follows the current by one-fourth of a cycle, or by a  phase angle.   
Since a capacitor can stop current when fully charged, it limits current and offers another form of AC resistance; Ohm’s law for a capacitor is  where  is the rms voltage across the capacitor.  is defined to be the capacitive reactance, given by    
•  has units of ohms and is greatest at low frequencies.

# 23.12 RLC Series AC Circuits

• The AC analogy to resistance is impedance  , the combined effect of resistors, inductors, and capacitors, defined by the AC version of Ohm’s law:  where  is the peak current and  is the peak source voltage. Impedance has units of ohms and is given by  .   
• The resonant frequency  , at which  , is  In an AC circuit, there is a phase angle  between source voltage  and the current  , which can be found from cos    
•  for a purely resistive circuit or an RLC circuit at resonance. The average power delivered to an  circuit is affected by the phase angle and is given by  cos  cos  is called the power factor, which ranges from 0 to 1.# Conceptual Questions

# 23.1 Induced Emf and Magnetic Flux

1. How do the multiple-loop coils and iron ring in the version of Faraday’s apparatus shown in Figure 23.3 enhance the observation of induced emf?   
2. When a magnet is thrust into a coil as in Figure 23.4(a), what is the direction of the force exerted by the coil on the magnet? Draw a diagram showing the direction of the current induced in the coil and the magnetic field it produces, to justify your response. How does the magnitude of the force depend on the resistance of the galvanometer?   
3. Explain how magnetic flux can be zero when the magnetic field is not zero.   
4. Is an emf induced in the coil in Figure 23.51 when it is stretched? If so, state why and give the direction of the induced current.

  
FIGURE 23.51 A circular coil of wire is stretched in a magnetic field.

# 23.2 Faraday’s Law of Induction: Lenz’s Law

5. A person who works with large magnets sometimes places her head inside a strong field. She reports feeling dizzy as she quickly turns her head. How might this be associated with induction? 6. A particle accelerator sends high-velocity charged particles down an evacuated pipe. Explain how a coil of wire wrapped around the pipe could detect the passage of individual particles. Sketch a graph of the voltage output of the coil as a single particle passes through it.

# 23.3 Motional Emf

7. Why must part of the circuit be moving relative to other parts, to have usable motional emf? Consider, for example, that the rails in Figure 23.10 are stationary relative to the magnetic field, while the rod moves.

8. A powerful induction cannon can be made by placing a metal cylinder inside a solenoid coil. The cylinder is forcefully expelled when solenoid current is turned on rapidly. Use Faraday’s and Lenz’s laws to explain how this works. Why might the cylinder get live/hot when the cannon is fired?   
9. An induction stove heats a pot with a coil carrying an alternating current located beneath the pot (and without a hot surface). Can the stove surface be a conductor? Why won’t a coil carrying a direct current work?   
10. Explain how you could thaw out a frozen water pipe by wrapping a coil carrying an alternating current around it. Does it matter whether or not the pipe is a conductor? Explain.

# 23.4 Eddy Currents and Magnetic Damping

11. Explain why magnetic damping might not be effective on an object made of several thin conducting layers separated by insulation.   
12. Explain how electromagnetic induction can be used to detect metals? This technique is particularly important in detecting buried landmines for disposal, geophysical prospecting and at airports.

# 23.5 Electric Generators

13. Using RHR-1, show that the emfs in the sides of the generator loop in Figure 23.22 are in the same sense and thus add.   
14. The source of a generator’s electrical energy output is the work done to turn its coils. How is the work needed to turn the generator related to Lenz’s law?

# 23.6 Back Emf

15. Suppose you find that the belt drive connecting a powerful motor to an air conditioning unit is broken and the motor is running freely. Should you be worried that the motor is consuming a great deal of energy for no useful purpose? Explain why or why not.

# 23.7 Transformers

16. Explain what causes physical vibrations in transformers at twice the frequency of the AC power involved.# 23.8 Electrical Safety: Systems and Devices

17. Does plastic insulation on live/hot wires prevent shock hazards, thermal hazards, or both?   
18. Why are ordinary circuit breakers and fuses ineffective in preventing shocks?   
19. A GFI may trip just because the live/hot and neutral wires connected to it are significantly different in length. Explain why.

# 23.9 Inductance

20. How would you place two identical flat coils in contact so that they had the greatest mutual inductance? The least?   
21. How would you shape a given length of wire to give it the greatest self-inductance? The least?   
22. Verify, as was concluded without proof in Example 23.7, that units of 

# 23.11 Reactance, Inductive and Capacitive

23. Presbycusis is a hearing loss due to age that progressively affects higher frequencies. A hearing aid amplifier is designed to amplify all frequencies equally. To adjust its output for presbycusis, would you put a capacitor in series or parallel with the hearing aid’s speaker? Explain.   
24. Would you use a large inductance or a large capacitance in series with a system to filter out low frequencies, such as the $ \mathsf { 1 0 0 } \mathsf { H z }$ hum in a sound system? Explain.   
25. High-frequency noise in AC power can damage computers. Does the plug-in unit designed to prevent this damage use a large inductance or a large capacitance (in series with the computer) to filter out such high frequencies? Explain.   
26. Does inductance depend on current, frequency, or both? What about inductive reactance?

27. Explain why the capacitor in Figure 23.52(a) acts as a low-frequency filter between the two circuits, whereas that in Figure 23.52(b) acts as a highfrequency filter.

  
FIGURE 23.52 Capacitors and inductors. Capacitor with high frequency and low frequency.

28. If the capacitors in Figure 23.52 are replaced by inductors, which acts as a low-frequency filter and which as a high-frequency filter?

# 23.12 RLC Series AC Circuits

29. Does the resonant frequency of an AC circuit depend on the peak voltage of the AC source? Explain why or why not.   
30. Suppose you have a motor with a power factor significantly less than 1. Explain why it would be better to improve the power factor as a method of improving the motor’s output, rather than to increase the voltage input.# Problems & Exercises

# 23.1 Induced Emf and Magnetic Flux

1. What is the value of the magnetic flux at coil 2 in Figure 23.53 due to coil 1?

  
FIGURE 23.53 (a) The planes of the two coils are perpendicular. (b) The wire is perpendicular to the plane of the coil.

2. What is the value of the magnetic flux through the coil in Figure 23.53(b) due to the wire?

# 23.2 Faraday’s Law of Induction: Lenz’s Law

3. Referring to Figure 23.54(a), what is the direction of the current induced in coil 2: (a) If the current in coil 1 increases? (b) If the current in coil 1 decreases? (c) If the current in coil 1 is constant? Explicitly show how you follow the steps in the Problem-Solving Strategy for Lenz's Law.

  
FIGURE 23.54 (a) The coils lie in the same plane. (b) The wire is in the plane of the coil

4. Referring to Figure 23.54(b), what is the direction of the current induced in the coil: (a) If the current in the wire increases? (b) If the current in the wire decreases? (c) If the current in the wire suddenly changes direction? Explicitly show how you follow the steps in the Problem-Solving Strategy for Lenz’s Law.

5. Referring to Figure 23.55, what are the directions of the currents in coils 1, 2, and 3 (assume that the coils are lying in the plane of the circuit): (a) When the switch is first closed? (b) When the switch has been closed for a long time? (c) Just after the switch is opened?

  
FIGURE 23.55

6. Repeat the previous problem with the battery reversed.   
7. Verify that the units of  are volts. That is, show that  .   
8. Suppose a 50-turn coil lies in the plane of the page in a uniform magnetic field that is directed into the page. The coil originally has an area of  . It is stretched to have no area in  . What is the direction and magnitude of the induced emf if the uniform magnetic field has a strength of 1.50 T?   
9. (a) An MRI technician moves his hand from a region of very low magnetic field strength into an MRI scanner’s 2.00 T field with his fingers pointing in the direction of the field. Find the average emf induced in his wedding ring, given its diameter is  and assuming it takes 0.250 s to move it into the field. (b) Discuss whether this current would significantly change the temperature of the ring.

10. Integrated Concepts Referring to the situation in the previous problem: (a) What current is induced in the ring if its resistance is  (b) What average power is dissipated? (c) What magnetic field is induced at the center of the ring? (d) What is the direction of the induced magnetic field relative to the MRI’s field?

11. An emf is induced by rotating a 1000-turn, 20.0 cm diameter coil in the Earth’s  T magnetic field. What average emf is induced, given the plane of the coil is originally perpendicular to the Earth’s field and is rotated to be parallel to the field in 12. A 0.250 m radius, 500-turn coil is rotated onefourth of a revolution in  , originally having its plane perpendicular to a uniform magnetic field. (This is 60 rev/s.) Find the magnetic field strength needed to induce an average emf of 10,000 V.

13. Integrated Concepts Approximately how does the emf induced in the loop in Figure 23.54(b) depend on the distance of the center of the loop from the wire?

14. Integrated Concepts (a) A lightning bolt produces a rapidly varying magnetic field. If the bolt strikes the earth vertically and acts like a current in a long straight wire, it will induce a voltage in a loop aligned like that in Figure 23.54(b). What voltage is induced in .  diameter loop  from a  lightning strike, if the current falls to zero in  (b) Discuss circumstances under which such a voltage would produce noticeable consequences.

# 23.3 Motional Emf

15. Use Faraday’s law, Lenz’s law, and RHR-1 to show that the magnetic force on the current in the moving rod in Figure 23.10 is in the opposite direction of its velocity.

16. If a current flows in the Satellite Tether shown in Figure 23.11, use Faraday’s law, Lenz’s law, and RHR-1 to show that there is a magnetic force on the tether in the direction opposite to its velocity.

17. (a) A jet airplane with a  wingspan is flying at  . What emf is induced between wing tips if the vertical component of the Earth’s field is  ? (b) Is an emf of this magnitude likely to have any consequences? Explain.

18. (a) A nonferrous screwdriver is being used in a  magnetic field. What maximum emf can be induced along its  length when it moves at  (b) Is it likely that this emf will have any consequences or even be noticed?

19. At what speed must the sliding rod in Figure 23.10 move to produce an emf of  in a 1.50 T field, given the rod’s length is 

20. The  long rod in Figure 23.10 moves at  . What is the strength of the magnetic field if a  emf is induced?

21. Prove that when  and  are not mutually perpendicular, motional emf is given by  sin  . If  is perpendicular to  , then  is the angle between  and  . If  is perpendicular to  , then  is the angle between  and  .

22. In the August 1992 space shuttle flight, only 250 m of the conducting tether considered in Example 23.2 could be let out. A  motional emf was generated in the Earth’s  field, while moving at  . What was the angle between the shuttle’s velocity and the Earth’s field, assuming the conductor was perpendicular to the field?

23. Integrated Concepts Derive an expression for the current in a system like that in Figure 23.10, under the following conditions. The resistance between the rails is  , the rails and the moving rod are identical in cross section  and have the same resistivity  . The distance between the rails is l, and the rod moves at constant speed  perpendicular to the uniform field  . At time zero, the moving rod is next to the resistance  .

24. Integrated Concepts The Tethered Satellite in Figure 23.11 has a mass of  and is at the end of a  long, 2.50 mm diameter cable with the tensile strength of steel. (a) How much does the cable stretch if a 100 N force is exerted to pull the satellite in? (Assume the satellite and shuttle are at the same altitude above the Earth.) (b) What is the effective force constant of the cable? (c) How much energy is stored in it when stretched by the  force?

25. Integrated Concepts The Tethered Satellite discussed in this module is producing  , and a current of 10.0 A flows. (a) What magnetic drag force does this produce if the system is moving at  (b) How much kinetic energy is removed from the system in 1.00 h, neglecting any change in altitude or velocity during that time? (c) What is the change in velocity if the mass of the system is  (d) Discuss the long term consequences (say, a weeklong mission) on the space shuttle’s orbit, noting what effect a decrease in velocity has and assessing the magnitude of the effect.

# 23.4 Eddy Currents and Magnetic Damping

26. Make a drawing similar to Figure 23.13, but with the pendulum moving in the opposite direction. Then use Faraday’s law, Lenz’s law, and RHR-1 to show that magnetic force opposes motion.  
FIGURE 23.56 A coil is moved into and out of a region of uniform magnetic field.

A coil is moved through a magnetic field as shown in Figure 23.56. The field is uniform inside the rectangle and zero outside. What is the direction of the induced current and what is the direction of the magnetic force on the coil at each position shown?

# 23.5 Electric Generators

28. Calculate the peak voltage of a generator that rotates its 200-turn,  diameter coil at 3600 rpm in a 0.800 T field.

29. At what angular velocity in rpm will the peak voltage of a generator be  if its 500-turn,  diameter coil rotates in a 0.250 T field?

30. What is the peak emf generated by rotating a 1000-turn,  diameter coil in the Earth’s  magnetic field, given the plane of the coil is originally perpendicular to the Earth’s field and is rotated to be parallel to the field in 

31. What is the peak emf generated by a  radius, 500-turn coil is rotated one-fourth of a revolution in  , originally having its plane perpendicular to a uniform magnetic field. (This is 60 rev/s.)

32. (a) A bicycle generator rotates at 1875 rad/s, producing an  peak emf. It has a 1.00 by  rectangular coil in a 0.640 T field. How many turns are in the coil? (b) Is this number of turns of wire practical for a 1.00 by 3.00 cm coil?

33. Integrated Concepts This problem refers to the bicycle generator considered in the previous problem. It is driven by a  diameter wheel that rolls on the outside rim of the bicycle tire. (a) What is the velocity of the bicycle if the generator’s angular velocity is  (b) What is the maximum emf of the generator when the bicycle moves at  , noting that it was  under the original conditions? (c) If the sophisticated generator can vary its own magnetic field, what field strength will it need at  to produce a  maximum emf?

34. (a) A car generator turns at 400 rpm when the engine is idling. Its 300-turn, 5.00 by  rectangular coil rotates in an adjustable magnetic field so that it can produce sufficient voltage even at low rpms. What is the field strength needed to produce a  peak emf? (b) Discuss how this required field strength compares to those available in permanent and electromagnets.

35. Show that if a coil rotates at an angular velocity  , the period of its AC output is  .

36. A 75-turn,  diameter coil rotates at an angular velocity of  in a  field, starting with the plane of the coil parallel to the field. (a) What is the peak emf? (b) At what time is the peak emf first reached? (c) At what time is the emf first at its most negative? (d) What is the period of the AC voltage output?

37. (a) If the emf of a coil rotating in a magnetic field is zero at  , and increases to its first peak at  , what is the angular velocity of the coil? (b) At what time will its next maximum occur? (c) What is the period of the output? (d) When is the output first one-fourth of its maximum? (e) When is it next one-fourth of its maximum?

38. Unreasonable Results A 500-turn coil with a  area is spun in the Earth’s  field, producing a 12.0 kV maximum emf. (a) At what angular velocity must the coil be spun? (b) What is unreasonable about this result? (c) Which assumption or premise is responsible?

# 23.6 Back Emf

39. Suppose a motor connected to a  source draws 10.0 A when it first starts. (a) What is its resistance? (b) What current does it draw at its normal operating speed when it develops a 100 V back emf?   
40. A motor operating on  electricity has a 180 V back emf at operating speed and draws a 12.0 A current. (a) What is its resistance? (b) What current does it draw when it is first started?   
41. What is the back emf of a  motor that draws 8.00 A at its normal speed and 20.0 A when first starting?   
42. The motor in a toy car operates on  , developing a 4.50 V back emf at normal speed. If it draws 3.00 A at normal speed, what current does it draw when starting?43. Integrated Concepts

The motor in a toy car is powered by four batteries in series, which produce a total emf of 6.00 V. The motor draws 3.00 A and develops a  back emf at normal speed. Each battery has a  internal resistance. What is the resistance of the motor?

# 23.7 Transformers

44. A plug-in transformer, like that in Figure 23.25, supplies  to a video game system. (a) How many turns are in its secondary coil, if its input voltage is  and the primary coil has 400 turns? (b) What is its input current when its output is 1.30 A?

45. An American traveler in New Zealand carries a transformer to convert New Zealand’s standard  to  so that she can use some small appliances on her trip. (a) What is the ratio of turns in the primary and secondary coils of her transformer? (b) What is the ratio of input to output current? (c) How could a New Zealander traveling in the United States use this same transformer to power her  appliances from 120 V?

46. A cassette recorder uses a plug-in transformer to convert  to  , with a maximum current output of  . (a) What is the current input? (b) What is the power input? (c) Is this amount of power reasonable for a small appliance?

47. (a) What is the voltage output of a transformer used for rechargeable flashlight batteries, if its primary has 500 turns, its secondary 4 turns, and the input voltage is 120 V? (b) What input current is required to produce a 4.00 A output? (c) What is the power input?

48. (a) The plug-in transformer for a laptop computer puts out  and can supply a maximum current of 2.00 A. What is the maximum input current if the input voltage is 240 V? Assume  efficiency. (b) If the actual efficiency is less than  , would the input current need to be greater or smaller? Explain.

49. A multipurpose transformer has a secondary coil with several points at which a voltage can be extracted, giving outputs of 5.60, 12.0, and  (a) The input voltage is  to a primary coil of 280 turns. What are the numbers of turns in the parts of the secondary used to produce the output voltages? (b) If the maximum input current is 5.00 A, what are the maximum output currents (each used alone)?

50. A large power plant generates electricity at 12.0 kV. Its old transformer once converted the voltage to  The secondary of this transformer is being replaced so that its output can be  for more efficient cross-country transmission on upgraded transmission lines. (a) What is the ratio of turns in the new secondary compared with the old secondary? (b) What is the ratio of new current output to old output (at  ) for the same power? (c) If the upgraded transmission lines have the same resistance, what is the ratio of new line power loss to old?

51. If the power output in the previous problem is 1000 MW and line resistance is  , what were the old and new line losses?

52. Unreasonable Results The  AC electricity from a power transmission line is fed into the primary coil of a transformer. The ratio of the number of turns in the secondary to the number in the primary is  . (a) What voltage is induced in the secondary? (b) What is unreasonable about this result? (c) Which assumption or premise is responsible?

53. Construct Your Own Problem Consider a double transformer to be used to create very large voltages. The device consists of two stages. The first is a transformer that produces a much larger output voltage than its input. The output of the first transformer is used as input to a second transformer that further increases the voltage. Construct a problem in which you calculate the output voltage of the final stage based on the input voltage of the first stage and the number of turns or loops in both parts of both transformers (four coils in all). Also calculate the maximum output current of the final stage based on the input current. Discuss the possibility of power losses in the devices and the effect on the output current and power.# 23.8 Electrical Safety: Systems and Devices

# 54. Integrated Concepts

A short circuit to the grounded metal case of an appliance occurs as shown in Figure 23.57. The person touching the case is wet and only has a  resistance to earth/ground. (a) What is the voltage on the case if  flows through the person? (b) What is the current in the short circuit if the resistance of the earth/ground wire is  (c) Will this trigger the 20.0 A circuit breaker supplying the appliance?

  
FIGURE 23.57 A person can be shocked even when the case of an appliance is grounded. The large short circuit current produces a voltage on the case of the appliance, since the resistance of the earth/ground wire is not zero.

# 23.9 Inductance

55. Two coils are placed close together in a physics lab to demonstrate Faraday’s law of induction. A current of 5.00 A in one is switched off in  , inducing a  emf in the other. What is their mutual inductance?

56. If two coils placed next to one another have a mutual inductance of  , what voltage is induced in one when the 2.00 A current in the other is switched off in 

57. The 4.00 A current through a  inductor is switched off in  . What is the emf induced opposing this?

58. A device is turned on and 3.00 A flows through it 0.100 ms later. What is the self-inductance of the device if an induced 150 V emf opposes this?

59. Starting with  , show that the units of inductance are  .

60. Camera flashes charge a capacitor to high voltage by switching the current through an inductor on and off rapidly. In what time must the 0.100 A current through a  inductor be switched on or off to induce a  emf?

61. A large research solenoid has a self-inductance of 25.0 H. (a) What induced emf opposes shutting it off when 100 A of current through it is switched off in  (b) How much energy is stored in the inductor at full current? (c) At what rate in watts must energy be dissipated to switch the current off in  (d) In view of the answer to the last part, is it surprising that shutting it down this quickly is difficult?

62. (a) Calculate the self-inductance of a 50.0 cm long,  diameter solenoid having 1000 loops. (b) How much energy is stored in this inductor when 20.0 A of current flows through it? (c) How fast can it be turned off if the induced emf cannot exceed 3.00 V?

63. A precision laboratory resistor is made of a coil of wire  in diameter and  long, and it has 500 turns. (a) What is its self-inductance? (b) What average emf is induced if the 12.0 A current through it is turned on in  (one-fourth of a cycle for  (c) What is its inductance if it is shortened to half its length and counter-wound (two layers of 250 turns in opposite directions)?

64. The heating coils in a hair dryer are  in diameter, have a combined length of  , and a total of 400 turns. (a) What is their total selfinductance assuming they act like a single solenoid? (b) How much energy is stored in them when 6.00 A flows? (c) What average emf opposes shutting them off if this is done in  (onefourth of a cycle for  )?

65. When the 20.0 A current through an inductor is turned off in  , an 800 V emf is induced, opposing the change. What is the value of the selfinductance?

66. How fast can the 150 A current through a 0.250 H inductor be shut off if the induced emf cannot exceed 75.0 V?

67. Integrated Concepts

A very large, superconducting solenoid such as one used in MRI scans, stores 1.00 MJ of energy in its magnetic field when 100 A flows. (a) Find its self-inductance. (b) If the coils “go normal,” they gain resistance and start to dissipate thermal energy. What temperature increase is produced if all the stored energy goes into heating the 1000 kg magnet, given its average specific heat is 68. Unreasonable Results

A  inductor has 100 A of current turned off in  . (a) What voltage is induced to oppose this? (b) What is unreasonable about this result? (c) Which assumption or premise is responsible?

# 23.10 RL Circuits

69. If you want a characteristic RL time constant of  , and you have a  resistor, what value of self-inductance is needed?

70. Your RL circuit has a characteristic time constant of 20.0 ns, and a resistance of  . (a) What is the inductance of the circuit? (b) What resistance would give you a 1.00 ns time constant, perhaps needed for quick response in an oscilloscope?

71. A large superconducting magnet, used for magnetic resonance imaging, has a  inductance. If you want current through it to be adjustable with a 1.00 s characteristic time constant, what is the minimum resistance of system?

72. Verify that after a time of  , the current for the situation considered in Example 23.9 will be 0.183 A as stated.

73. Suppose you have a supply of inductors ranging from  to  , and resistors ranging from  to  . What is the range of characteristic  time constants you can produce by connecting a single resistor to a single inductor?

74. (a) What is the characteristic time constant of a  inductor that has a resistance of  (b) If it is connected to a  battery, what is the current after 

75. What percentage of the final current  flows through an inductor  in series with a resistor  , three time constants after the circuit is completed?

76. The 5.00 A current through a 1.50 H inductor is dissipated by a  resistor in a circuit like that in Figure 23.42 with the switch in position 2. (a) What is the initial energy in the inductor? (b) How long will it take the current to decline to  of its initial value? (c) Calculate the average power dissipated, and compare it with the initial power dissipated by the resistor.

77. (a) Use the exact exponential treatment to find how much time is required to bring the current through an  inductor in series with a  resistor to  of its final value, starting from zero. (b) Compare your answer to the approximate treatment using integral numbers of . (c) Discuss how significant the difference is.

78. (a) Using the exact exponential treatment, find the time required for the current through a  inductor in series with a  resistor to be reduced to  of its original value. (b) Compare your answer to the approximate treatment using integral numbers of  . (c) Discuss how significant the difference is.

# 23.11 Reactance, Inductive and Capacitive

79. At what frequency will a  inductor have a reactance of 

80. What value of inductance should be used if a  reactance is needed at a frequency of 

81. What capacitance should be used to produce a  reactance at 

82. At what frequency will an  capacitor have a reactance of 

83. (a) Find the current through a 0.500 H inductor connected to a  , 480 V AC source. (b) What would the current be at 

84. (a) What current flows when a  , 480 V AC source is connected to a  capacitor? (b) What would the current be at 

85. A  , 16.0 V source connected to an inductor produces a 2.00 A current. What is the inductance?

86. A  ,  source produces a  current when connected to a capacitor. What is the capacitance?

87. (a) An inductor designed to filter high-frequency noise from power supplied to a personal computer is placed in series with the computer. What minimum inductance should it have to produce a  reactance for  noise? (b) What is its reactance at 

88. The capacitor in Figure 23.52(a) is designed to filter low-frequency signals, impeding their transmission between circuits. (a) What capacitance is needed to produce a  reactance at a frequency of  (b) What would its reactance be at  (c) Discuss the implications of your answers to (a) and (b).89. The capacitor in Figure 23.52(b) will filter highfrequency signals by shorting them to earth/ ground. (a) What capacitance is needed to produce a reactance of  for a  signal? (b) What would its reactance be at 3.00  (c) Discuss the implications of your answers to (a) and (b).

90. Unreasonable Results In a recording of voltages due to brain activity (an EEG), a  signal with a  frequency is applied to a capacitor, producing a current of  . Resistance is negligible. (a) What is the capacitance? (b) What is unreasonable about this result? (c) Which assumption or premise is responsible?

91. Construct Your Own Problem Consider the use of an inductor in series with a computer operating on  electricity. Construct a problem in which you calculate the relative reduction in voltage of incoming high frequency noise compared to  voltage. Among the things to consider are the acceptable series reactance of the inductor for  power and the likely frequencies of noise coming through the power lines.

# 23.12 RLC Series AC Circuits

92. An RL circuit consists of a  resistor and a  inductor. (a) Find its impedance  at  and  . (b) Compare these values of  with those found in Example 23.12 in which there was also a capacitor.

93. An RC circuit consists of a  resistor and a  capacitor. (a) Find its impedance at 60.0  and  . (b) Compare these values of  with those found in Example 23.12, in which there was also an inductor.

94. An LC circuit consists of a  inductor and a  capacitor. (a) Find its impedance at 60.0 Hz and  . (b) Compare these values of  with those found in Example 23.12 in which there was also a resistor.

95. What is the resonant frequency of a  inductor connected to a  capacitor?

96. To receive AM radio, you want an RLC circuit that can be made to resonate at any frequency between 500 and  . This is accomplished with a fixed  inductor connected to a variable capacitor. What range of capacitance is needed?

97. Suppose you have a supply of inductors ranging from  to  , and capacitors ranging from 1.00 pF to 0.100 F. What is the range of resonant frequencies that can be achieved from combinations of a single inductor and a single capacitor?

98. What capacitance do you need to produce a resonant frequency of  , when using an  inductor?

99. What inductance do you need to produce a resonant frequency of  , when using a  capacitor?

100. The lowest frequency in the FM radio band is  . (a) What inductance is needed to produce this resonant frequency if it is connected to a 2.50 pF capacitor? (b) The capacitor is variable, to allow the resonant frequency to be adjusted to as high as  . What must the capacitance be at this frequency?

101. An RLC series circuit has a  resistor, a  inductor, and an  capacitor.(a) Find the circuit’s impedance at $ \mathsf { 1 2 0 } \mathsf { H z }$ . (b) Find the circuit’s impedance at  . (c) If the voltage source has  , what is  at each frequency? (d) What is the resonant frequency of the circuit? (e) What is  at resonance?

102. An RLC series circuit has a  resistor, a  inductor, and a 25.0 nF capacitor. (a) Find the circuit’s impedance at  . (b) Find the circuit’s impedance at  . (c) If the voltage source has  , what is  at each frequency? (d) What is the resonant frequency of the circuit? (e) What is  at resonance?

103. An RLC series circuit has a  resistor, a  inductor, and an  capacitor. (a) Find the power factor at  . (b) What is the phase angle at  (c) What is the average power at  (d) Find the average power at the circuit’s resonant frequency.

104. An RLC series circuit has a  resistor, a  inductor, and a 25.0 nF capacitor. (a) Find the power factor at  . (b) What is the phase angle at this frequency? (c) What is the average power at this frequency? (d) Find the average power at the circuit’s resonant frequency.

105. An RLC series circuit has a  resistor and a  inductor. At  , the phase angle is  . (a) What is the impedance? (b) Find the circuit’s capacitance. (c) If  is applied, what is the average power supplied?106. Referring to Example 23.14, find the average power at  .

07. Critical Thinking A length of  of wire is to be used to detect a magnetic field. The wire is made into a single square loop and rotated at a rate of 400 cycles per second. (a) If the magnetic field is 0.02000 T, what is the magnitude of the average emf that can be generated in the first quarter cycle, provided the loop is initially oriented in a plane perpendicular to the magnetic field? (b) Is there a difference in the magnitude of the average emf generated if the wire is made into two square loops and rotated at the same rate, starting with the same orientation of the loops as that of the loop in part a? If so, what is the average emf possible for the first quarter cycle for two loops being rotated at 400 cycles per second in the magnetic field? (c) If the wire is made into a figure eight, what is the average emf for the first quarter cycle that can be generated by rotating it at 400 cycles per second in the magnetic field, again starting with the same orientation of the oops with respect to the magnetic field? The wire crosses itself in this arrangement. (d) Does the shape of the loop matter?