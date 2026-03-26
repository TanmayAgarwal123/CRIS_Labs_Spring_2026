# Chapter 12 - Fluid Dynamics and Its Biological and Medical Applications

  
FIGURE 12.1 Many fluids are flowing in this scene. Water from the hose and smoke from the fire are visible flows. Less visible are the flow of air and the flow of fluids on the ground and within the people fighting the fire. (credit: Andrew Magill, Flickr)

# CHAPTER OUTLINE

12.1 Flow Rate and Its Relation to Velocity   
12.2 Bernoulli’s Equation   
12.3 The Most General Applications of Bernoulli’s Equation   
12.4 Viscosity and Laminar Flow; Poiseuille’s Law   
12.5 The Onset of Turbulence   
12.6 Motion of an Object in a Viscous Fluid   
12.7 Molecular Transport Phenomena: Diffusion, Osmosis, and Related Processes

INTRODUCTION TO FLUID DYNAMICS AND ITS BIOLOGICAL AND MEDICAL APPLICATIONS We have dealt with many situations in which fluids are static. But by their very definition, fluids flow. Examples come easily—a column of smoke rises from a camp fire, water streams from a fire hose, blood courses through your veins. Why does rising smoke curl and twist? How does a nozzle increase the speed of water emerging from a hose? How does the body regulate blood flow? The physics of fluids in motion—fluid dynamics—allows us to answer these and many other questions.

Click to view content (https://openstax.org/books/college-physics-2e/pages/12-introduction-to-fluid-dynamicsand-its-biological-and-medical-applications)# 12.1 Flow Rate and Its Relation to Velocity

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Calculate flow rate.   
Define units of volume.   
Describe incompressible fluids.   
Explain the consequences of the equation of continuity.

Flow rate  is defined to be the volume of fluid passing by some location through an area during a period of time, as seen in Figure 12.2. In symbols, this can be written as



where  is the volume and  is the elapsed time.

The SI unit for flow rate is  , but a number of other units for  are in common use. For example, the heart of a resting adult pumps blood at a rate of 5.00 liters per minute  . Note that a liter (L) is 1/1000 of a cubic meter or 1000 cubic centimeters  or  ). In this text we shall use whatever metric units are most convenient for a given situation.

  
FIGURE 12.2 Flow rate is the volume of fluid per unit time flowing past a point through the area  . Here the shaded cylinder of fluid flows past point in a uniform pipe in time . The volume of the cylinder is  and the average velocity is  so that the flow rate is  .

# EXAMPLE 12.1

# Calculating Volume from Flow Rate: The Heart Pumps a Lot of Blood in a Lifetime

How many cubic meters of blood does the heart pump in a 75-year lifetime, assuming the average flow rate is 5.00 L/min?

# Strategy

Time and flow rate  are given, and so the volume  can be calculated from the definition of flow rate.

# Solution

Solving  for volume gives



Substituting known values yields



# Discussion

This amount is about 200,000 tons of blood. For comparison, this value is equivalent to about 200 times the volume of water contained in a 6-lane  lap pool.Flow rate and velocity are related, but quite different, physical quantities. To make the distinction clear, think about the flow rate of a river. The greater the velocity of the water, the greater the flow rate of the river. But flow rate also depends on the size of the river. A rapid mountain stream carries far less water than the Amazon River in Brazil, for example. The precise relationship between flow rate  and velocity  is



where  is the cross-sectional area and  is the average velocity. This equation seems logical enough. The relationship tells us that flow rate is directly proportional to both the magnitude of the average velocity (hereafter referred to as the speed) and the size of a river, pipe, or other conduit. The larger the conduit, the greater its crosssectional area. Figure 12.2 illustrates how this relationship is obtained. The shaded cylinder has a volume



which flows past the point  in a time  . Dividing both sides of this relationship by  gives



We note that  and the average speed is  . Thus the equation becomes  .

Figure 12.3 shows an incompressible fluid flowing along a pipe of decreasing radius. Because the fluid is incompressible, the same amount of fluid must flow past any point in the tube in a given time to ensure continuity of flow. In this case, because the cross-sectional area of the pipe decreases, the velocity must necessarily increase. This logic can be extended to say that the flow rate must be the same at all points along the pipe. In particular, for points 1 and 2,



This is called the equation of continuity and is valid for any incompressible fluid. The consequences of the equation of continuity can be observed when water flows from a hose into a narrow spray nozzle: it emerges with a large speed—that is the purpose of the nozzle. Conversely, when a river empties into one end of a reservoir, the water slows considerably, perhaps picking up speed again when it leaves the other end of the reservoir. In other words, speed increases when cross-sectional area decreases, and speed decreases when cross-sectional area increases.

  
FIGURE 12.3 When a tube narrows, the same volume occupies a greater length. For the same volume to pass points 1 and 2 in a given time, the speed must be greater at point 2. The process is exactly reversible. If the fluid flows in the opposite direction, its speed will decrease when the tube widens. (Note that the relative volumes of the two cylinders and the corresponding velocity vector arrows are not drawn to scale.)

Since liquids are essentially incompressible, the equation of continuity is valid for all liquids. However, gases are compressible, and so the equation must be applied with caution to gases if they are subjected to compression or expansion.

# EXAMPLE 12.2

# Calculating Fluid Speed: Speed Increases When a Tube Narrows

A nozzle with a radius of  is attached to a garden hose with a radius of  . The flow rate through hose and nozzle is 0.500 L/s. Calculate the speed of the water (a) in the hose and (b) in the nozzle.# Strategy

We can use the relationship between flow rate and speed to find both velocities. We will use the subscript 1 for the hose and 2 for the nozzle.

# Solution for (a)

First, we solve  for  and note that the cross-sectional area is  , yielding



Substituting known values and making appropriate unit conversions yields



# Solution for (b)

We could repeat this calculation to find the speed in the nozzle  , but we will use the equation of continuity to give a somewhat different insight. Using the equation which states



solving for  and substituting  for the cross-sectional area yields



Substituting known values,



# Discussion

A speed of  is about right for water emerging from a nozzleless hose. The nozzle produces a considerably faster stream merely by constricting the flow to a narrower tube.

The solution to the last part of the example shows that speed is inversely proportional to the square of the radius of the tube, making for large effects when radius varies. We can blow out a candle at quite a distance, for example, by pursing our lips, whereas blowing on a candle with our mouth wide open is quite ineffective.

In many situations, including in the cardiovascular system, branching of the flow occurs. The blood is pumped from the heart into arteries that subdivide into smaller arteries (arterioles) which branch into very fine vessels called capillaries. In this situation, continuity of flow is maintained but it is the sum of the flow rates in each of the branches in any portion along the tube that is maintained. The equation of continuity in a more general form becomes



where  and  are the number of branches in each of the sections along the tube.

# EXAMPLE 12.3

# Calculating Flow Speed and Vessel Diameter: Branching in the Cardiovascular System

The aorta is the principal blood vessel through which blood leaves the heart in order to circulate around the body. (a) Calculate the average speed of the blood in the aorta if the flow rate is  . The aorta has a radius of  . (b) Blood also flows through smaller blood vessels known as capillaries. When the rate of blood flow in the aorta is , the speed of blood in the capillaries is about  . Given that the average diameter of a capillary is  , calculate the number of capillaries in the blood circulatory system.

# Strategy

We can use  to calculate the speed of flow in the aorta and then use the general form of the equation of continuity to calculate the number of capillaries as all of the other variables are known.

# Solution for (a)

The flow rate is given by  or  for a cylindrical vessel.

Substituting the known values (converted to units of meters and seconds) gives



# Solution for (b)

Using  , assigning the subscript 1 to the aorta and 2 to the capillaries, and solving for  (the number of capillaries) gives  . Converting all quantities to units of meters and seconds and substituting into the equation above gives



# Discussion

Note that the speed of flow in the capillaries is considerably reduced relative to the speed in the aorta due to the significant increase in the total cross-sectional area at the capillaries. This low speed is to allow sufficient time for effective exchange to occur although it is equally important for the flow not to become stationary in order to avoid the possibility of clotting. Does this large number of capillaries in the body seem reasonable? In active muscle, one finds about 200 capillaries per  , or about  per  of muscle. For  of muscle, this amounts to about  capillaries.

# 12.2 Bernoulli’s Equation

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Explain the terms in Bernoulli’s equation.   
Explain how Bernoulli’s equation is related to conservation of energy.   
Explain how to derive Bernoulli’s principle from Bernoulli’s equation.   
Calculate with Bernoulli’s principle.   
List some applications of Bernoulli’s principle.

When a fluid flows into a narrower channel, its speed increases. That means its kinetic energy also increases. Where does that change in kinetic energy come from? The increased kinetic energy comes from the net work done on the fluid to push it into the channel and the work done on the fluid by the gravitational force, if the fluid changes vertical position. Recall the work-energy theorem,



There is a pressure difference when the channel narrows. This pressure difference results in a net force on the fluid: recall that pressure times area equals force. The net work done increases the fluid’s kinetic energy. As a result, the pressure will drop in a rapidly-moving fluid, whether or not the fluid is confined to a tube.

There are a number of common examples of pressure dropping in rapidly-moving fluids. Shower curtains have adisagreeable habit of bulging into the shower stall when the shower is on. The high-velocity stream of water and air creates a region of lower pressure inside the shower, and standard atmospheric pressure on the other side. The pressure difference results in a net force inward pushing the curtain in. You may also have noticed that when passing a truck on the highway, your car tends to veer toward it. The reason is the same—the high velocity of the air between the car and the truck creates a region of lower pressure, and the vehicles are pushed together by greater pressure on the outside. (See Figure 12.4.) This effect was observed as far back as the mid-1800s, when it was found that trains passing in opposite directions tipped precariously toward one another.

  
FIGURE 12.4 An overhead view of a car passing a truck on a highway. Air passing between the vehicles flows in a narrower channel and must increase its speed  is greater than  ), causing the pressure between them to drop  is less than  ). Greater pressure on the outside pushes the car and truck together.

# Making Connections: Take-Home Investigation with a Sheet of Paper

Hold the short edge of a sheet of paper parallel to your mouth with one hand on each side of your mouth. The page should slant downward over your hands. Blow over the top of the page. Describe what happens and explain the reason for this behavior.

# Bernoulli’s Equation

The relationship between pressure and velocity in fluids is described quantitatively by Bernoulli’s equation, named after its discoverer, the Swiss scientist Daniel Bernoulli (1700–1782). Bernoulli’s equation states that for an incompressible, frictionless fluid, the following sum is constant:



where  is the absolute pressure,  is the fluid density,  is the velocity of the fluid,  is the height above some reference point, and  is the acceleration due to gravity. If we follow a small volume of fluid along its path, various quantities in the sum may change, but the total remains constant. Let the subscripts 1 and 2 refer to any two points along the path that the bit of fluid follows; Bernoulli’s equation becomes



Bernoulli’s equation is a form of the conservation of energy principle. Note that the second and third terms are the kinetic and potential energy with  replaced by  . In fact, each term in the equation has units of energy per unit volume. We can prove this for the second term by substituting  into it and gathering terms:



 is the kinetic energy per unit volume. Making the same substitution into the third term in the equation, we find

so  is the gravitational potential energy per unit volume. Note that pressure  has units of energy per unit volume, too. Since  , its units are  . If we multiply these by  , we obtain  , or energy per unit volume. Bernoulli’s equation is, in fact, just a convenient statement of conservation of energy for an incompressible fluid in the absence of friction.

# Making Connections: Conservation of Energy

Conservation of energy applied to fluid flow produces Bernoulli’s equation. The net work done by the fluid’s pressure results in changes in the fluid’s and  per unit volume. If other forms of energy are involved in fluid flow, Bernoulli’s equation can be modified to take these forms into account. Such forms of energy include thermal energy dissipated because of fluid viscosity.

The general form of Bernoulli’s equation has three terms in it, and it is broadly applicable. To understand it better, we will look at a number of specific situations that simplify and illustrate its use and meaning.

# Bernoulli’s Equation for Static Fluids

Let us first consider the very simple situation where the fluid is static—that is,  . Bernoulli’s equation in that case is



We can further simplify the equation by taking  (we can always choose some height to be zero, just as we often have done for other situations involving the gravitational force, and take all other heights to be relative to this). In that case, we get



This equation tells us that, in static fluids, pressure increases with depth. As we go from point 1 to point 2 in the fluid, the depth increases by  , and consequently,  is greater than  by an amount  . In the very simplest case,  is zero at the top of the fluid, and we get the familiar relationship  . (Recall that  and  Bernoulli’s equation includes the fact that the pressure due to the weight of a fluid is  . Although we introduce Bernoulli’s equation for fluid flow, it includes much of what we studied for static fluids in the preceding chapter.

# Bernoulli’s Principle—Bernoulli’s Equation at Constant Depth

Another important situation is one in which the fluid moves but its depth is constant—that is,  . Under that condition, Bernoulli’s equation becomes



Situations in which fluid flows at a constant depth are so important that this equation is often called Bernoulli’s principle. It is Bernoulli’s equation for fluids at constant depth. (Note again that this applies to a small volume of fluid as we follow it along its path.) As we have just discussed, pressure drops as speed increases in a moving fluid. We can see this from Bernoulli’s principle. For example, if  is greater than  in the equation, then  must be less than  for the equality to hold.

# EXAMPLE 12.4

# Calculating Pressure: Pressure Drops as a Fluid Speeds Up

In Example 12.2, we found that the speed of water in a hose increased from  to  going from the hose to the nozzle. Calculate the pressure in the hose, given that the absolute pressure in the nozzle is  (atmospheric, as it must be) and assuming level, frictionless flow.# Strategy

Level flow means constant depth, so Bernoulli’s principle applies. We use the subscript 1 for values in the hose and 2 for those in the nozzle. We are thus asked to find  .

# Solution

Solving Bernoulli’s principle for  yields



Substituting known values,



# Discussion

This absolute pressure in the hose is greater than in the nozzle, as expected since  is greater in the nozzle. The pressure  in the nozzle must be atmospheric since it emerges into the atmosphere without other changes in conditions.

# Applications of Bernoulli’s Principle

There are a number of devices and situations in which fluid flows at a constant height and, thus, can be analyzed with Bernoulli’s principle.

# Entrainment

People have long put the Bernoulli principle to work by using reduced pressure in high-velocity fluids to move things about. With a higher pressure on the outside, the high-velocity fluid forces other fluids into the stream. This process is called entrainment. Entrainment devices have been in use since ancient times, particularly as pumps to raise water small heights, as in draining swamps, fields, or other low-lying areas. Some other devices that use the concept of entrainment are shown in Figure 12.5.

  
FIGURE 12.5 Examples of entrainment devices that use increased fluid speed to create low pressures, which then entrain one fluid into another. (a) A Bunsen burner uses an adjustable gas nozzle, entraining air for proper combustion. (b) An atomizer uses a squeeze bulb to create a jet of air that entrains drops of perfume. Paint sprayers and carburetors use very similar techniques to move their respective liquids. (c) A common aspirator uses a high-speed stream of water to create a region of lower pressure. Aspirators may be used as suction pumps in dental and surgical situations or for draining a flooded basement or producing a reduced pressure in a vessel. (d) The chimney of a water heater is designed to entrain air into the pipe leading through the ceiling.

# Wings and Sails

The airplane wing is a beautiful example of Bernoulli’s principle in action. Figure 12.6(a) shows the characteristic shape of a wing. The wing is tilted upward at a small angle and the upper surface is longer, causing air to flow faster over it. The pressure on top of the wing is therefore reduced, creating a net upward force or lift. (Wings can also gain lift by pushing air downward, utilizing the conservation of momentum principle. The deflected air molecules result in an upward force on the wing — Newton’s third law.) Sails also have the characteristic shape of a wing. (See Figure 12.6(b).) The pressure on the front side of the sail,  , is lower than the pressure on the back of the sail,  .This results in a forward force and even allows you to sail into the wind.

# Making Connections: Take-Home Investigation with Two Strips of Paper

For a good illustration of Bernoulli’s principle, make two strips of paper, each about  long and 4 cm wide. Hold the small end of one strip up to your lips and let it drape over your finger. Blow across the paper. What happens? Now hold two strips of paper up to your lips, separated by your fingers. Blow between the strips. What happens?

# Velocity measurement

Figure 12.7 shows two devices that measure fluid velocity based on Bernoulli’s principle. The manometer in Figure 12.7(a) is connected to two tubes that are small enough not to appreciably disturb the flow. The tube facing the oncoming fluid creates a dead spot having zero velocity  ) in front of it, while fluid passing the other tube has velocity  . This means that Bernoulli’s principle as stated in  becomes



  
FIGURE 12.6 (a) The Bernoulli principle helps explain lift generated by a wing. (b) Sails use the same technique to generate part of their thrust.

Thus pressure  over the second opening is reduced by  , and so the fluid in the manometer rises by  on the side connected to the second opening, where



(Recall that the symbol means “proportional to.”) Solving for  , we see that



Figure 12.7(b) shows a version of this device that is in common use for measuring various fluid velocities; such devices are frequently used as air speed indicators in aircraft.  
FIGURE 12.7 Measurement of fluid speed based on Bernoulli’s principle. (a) A manometer is connected to two tubes that are close together and small enough not to disturb the flow. Tube 1 is open at the end facing the flow. A dead spot having zero speed is created there. Tube 2 has an opening on the side, and so the fluid has a speed  across the opening; thus, pressure there drops. The difference in pressure at the manometer is  , and so  is proportional to  . (b) This type of velocity measuring device is a Prandtl tube, also known as a pitot tube.

# 12.3 The Most General Applications of Bernoulli’s Equation

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Calculate using Torricelli’s theorem. • Calculate power in fluid flow.

# Torricelli’s Theorem

Figure 12.8 shows water gushing from a large tube through a dam. What is its speed as it emerges? Interestingly, if resistance is negligible, the speed is just what it would be if the water fell a distance  from the surface of the reservoir; the water’s speed is independent of the size of the opening. Let us check this out. Bernoulli’s equation must be used since the depth is not constant. We consider water flowing from the surface (point 1) to the tube’s outlet (point 2). Bernoulli’s equation as stated in previously is



Both  and  equal atmospheric pressure  is atmospheric pressure because it is the pressure at the top of the reservoir.  must be atmospheric pressure, since the emerging water is surrounded by the atmosphere and cannot have a pressure different from atmospheric pressure.) and subtract out of the equation, leaving



Solving this equation for  , noting that the density  cancels (because the fluid is incompressible), yields



We let  ; the equation then becomes



where  is the height dropped by the water. This is simply a kinematic equation for any object falling a distance  with negligible resistance. In fluids, this last equation is called Torricelli’s theorem. Note that the result is independent of the velocity’s direction, just as we found when applying conservation of energy to falling objects.  
FIGURE 12.8 (a) Water gushes from the base of the Studen Kladenetz dam in Bulgaria. (credit: Kiril Kapustin; http://www.ImagesFromBulgaria.com) (b) In the absence of significant resistance, water flows from the reservoir with the same speed it would have if it fell the distance  without friction. This is an example of Torricelli’s theorem.

  
FIGURE 12.9 Pressure in the nozzle of this fire hose is less than at ground level for two reasons: the water has to go uphill to get to the nozzle, and speed increases in the nozzle. In spite of its lowered pressure, the water can exert a large force on anything it strikes, by virtue of its kinetic energy. Pressure in the water stream becomes equal to atmospheric pressure once it emerges into the air.

All preceding applications of Bernoulli’s equation involved simplifying conditions, such as constant height or constant pressure. The next example is a more general application of Bernoulli’s equation in which pressure,# EXAMPLE 12.5

# Calculating Pressure: A Fire Hose Nozzle

Fire hoses used in major structure fires have inside diameters of  . Suppose such a hose carries a flow of  starting at a gauge pressure of  . The hose goes  up a ladder to a nozzle having an inside diameter of  . Assuming negligible resistance, what is the pressure in the nozzle?

# Strategy

Here we must use Bernoulli’s equation to solve for the pressure, since depth is not constant.

# Solution

Bernoulli’s equation states



where the subscripts 1 and 2 refer to the initial conditions at ground level and the final conditions inside the nozzle, respectively. We must first find the speeds  and  . Since  , we get



Similarly, we find



(This rather large speed is helpful in reaching the fire.) Now, taking  to be zero, we solve Bernoulli’s equation for  :



Substituting known values yields



# Discussion

This value is a gauge pressure, since the initial pressure was given as a gauge pressure. Thus the nozzle pressure is very close to atmospheric pressure, as it must because the water exits into the atmosphere without changes in its conditions.

# Power in Fluid Flow

Power is the rate at which work is done or energy in any form is used or supplied. To see the relationship of power to fluid flow, consider Bernoulli’s equation:



All three terms have units of energy per unit volume, as discussed in the previous section. Now, considering units, if we multiply energy per unit volume by flow rate (volume per unit time), we get units of power. That is,  . This means that if we multiply Bernoulli’s equation by flow rate  , we get power. In equation form, this is

Each term has a clear physical meaning. For example,  is the power supplied to a fluid, perhaps by a pump, to give it its pressure  . Similarly,  is the power supplied to a fluid to give it its kinetic energy. And  is the power going to gravitational potential energy.

# Making Connections: Power

Power is defined as the rate of energy transferred, or  . Fluid flow involves several types of power. Each type of power is identified with a specific type of energy being expended or changed in form.

# EXAMPLE 12.6

# Calculating Power in a Moving Fluid

Suppose the fire hose in the previous example is fed by a pump that receives water through a hose with a  diameter coming from a hydrant with a pressure of  . What power does the pump supply to the water?

# Strategy

Here we must consider energy forms as well as how they relate to fluid flow. Since the input and output hoses have the same diameters and are at the same height, the pump does not change the speed of the water nor its height, and so the water’s kinetic energy and gravitational potential energy are unchanged. That means the pump only supplies power to increase water pressure by  (from  to  ).

# Solution

As discussed above, the power associated with pressure is



# Discussion

Such a substantial amount of power requires a large pump, such as is found on some fire trucks. (This kilowatt value converts to about 50 hp.) The pump in this example increases only the water’s pressure. If a pump—such as the heart—directly increases velocity and height as well as pressure, we would have to calculate all three terms to find the power it supplies.

# 12.4 Viscosity and Laminar Flow; Poiseuille’s Law

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Define laminar flow and turbulent flow.   
Explain what viscosity is.   
Calculate flow and resistance with Poiseuille’s law.   
Explain how pressure drops due to resistance.

# Laminar Flow and Viscosity

When you pour yourself a glass of juice, the liquid flows freely and quickly. But when you pour syrup on your pancakes, that liquid flows slowly and sticks to the pitcher. The difference is fluid friction, both within the fluid itself and between the fluid and its surroundings. We call this property of fluids viscosity. Juice has low viscosity, whereassyrup has high viscosity. In the previous sections we have considered ideal fluids with little or no viscosity. In this section, we will investigate what factors, including viscosity, affect the rate of fluid flow.

The precise definition of viscosity is based on laminar, or nonturbulent, flow. Before we can define viscosity, then, we need to define laminar flow and turbulent flow. Figure 12.10 shows both types of flow. Laminar flow is characterized by the smooth flow of the fluid in layers that do not mix. Turbulent flow, or turbulence, is characterized by eddies and swirls that mix layers of fluid together.

  
FIGURE 12.10 Smoke rises smoothly for a while and then begins to form swirls and eddies. The smooth flow is called laminar flow, whereas the swirls and eddies typify turbulent flow. If you watch the smoke (being careful not to breathe on it), you will notice that it rises more rapidly when flowing smoothly than after it becomes turbulent, implying that turbulence poses more resistance to flow. (credit: Creativity103)

Figure 12.11 shows schematically how laminar and turbulent flow differ. Layers flow without mixing when flow is laminar. When there is turbulence, the layers mix, and there are significant velocities in directions other than the overall direction of flow. The lines that are shown in many illustrations are the paths followed by small volumes of fluids. These are called streamlines. Streamlines are smooth and continuous when flow is laminar, but break up and mix when flow is turbulent. Turbulence has two main causes. First, any obstruction or sharp corner, such as in a faucet, creates turbulence by imparting velocities perpendicular to the flow. Second, high speeds cause turbulence. The drag both between adjacent layers of fluid and between the fluid and its surroundings forms swirls and eddies, if the speed is great enough. We shall concentrate on laminar flow for the remainder of this section, leaving certain aspects of turbulence for later sections.

  
FIGURE 12.11 (a) Laminar flow occurs in layers without mixing. Notice that viscosity causes drag between layers as well as with the fixed surface. (b) An obstruction in the vessel produces turbulence. Turbulent flow mixes the fluid. There is more interaction, greater heating, and more resistance than in laminar flow.# Making Connections: Take-Home Experiment: Go Down to the River

Try dropping simultaneously two sticks into a flowing river, one near the edge of the river and one near the middle. Which one travels faster? Why?

Figure 12.12 shows how viscosity is measured for a fluid. Two parallel plates have the specific fluid between them. The bottom plate is held fixed, while the top plate is moved to the right, dragging fluid with it. The layer (or lamina) of fluid in contact with either plate does not move relative to the plate, and so the top layer moves at  while the bottom layer remains at rest. Each successive layer from the top down exerts a force on the one below it, trying to drag it along, producing a continuous variation in speed from  to 0 as shown. Care is taken to insure that the flow is laminar; that is, the layers do not mix. The motion in Figure 12.12 is like a continuous shearing motion. Fluids have zero shear strength, but the rate at which they are sheared is related to the same geometrical factors  and  as is shear deformation for solids.

  
FIGURE 12.12 The graphic shows laminar flow of fluid between two plates of area  . The bottom plate is fixed. When the top plate is pushed to the right, it drags the fluid along with it.

A force  is required to keep the top plate in Figure 12.12 moving at a constant velocity  , and experiments have shown that this force depends on four factors. First,  is directly proportional to  (until the speed is so high that turbulence occurs—then a much larger force is needed, and it has a more complicated dependence on  ). Second,  is proportional to the area  of the plate. This relationship seems reasonable, since  is directly proportional to the amount of fluid being moved. Third,  is inversely proportional to the distance between the plates  . This relationship is also reasonable;  is like a lever arm, and the greater the lever arm, the less force that is needed. Fourth,  is directly proportional to the coefficient of viscosity,  . The greater the viscosity, the greater the force required. These dependencies are combined into the equation



which gives us a working definition of fluid viscosity  . Solving for  gives



which defines viscosity in terms of how it is measured. The SI unit of viscosity is  or  Table 12.1 lists the coefficients of viscosity for various fluids.

Viscosity varies from one fluid to another by several orders of magnitude. As you might expect, the viscosities of gases are much less than those of liquids, and these viscosities are often temperature dependent. The viscosity of blood can be reduced by aspirin consumption, allowing it to flow more easily around the body. (When used over the long term in low doses, aspirin can help prevent heart attacks, and reduce the risk of blood clotting.)

# Laminar Flow Confined to Tubes—Poiseuille’s Law

What causes flow? The answer, not surprisingly, is pressure difference. In fact, there is a very simple relationship between horizontal flow and pressure. Flow rate  is in the direction from high to low pressure. The greater the pressure differential between two points, the greater the flow rate. This relationship can be stated as

where  and  are the pressures at two points, such as at either end of a tube, and  is the resistance to flow. The resistance  includes everything, except pressure, that affects flow rate. For example,  is greater for a long tube than for a short one. The greater the viscosity of a fluid, the greater the value of  . Turbulence greatly increases  , whereas increasing the diameter of a tube decreases  .

If viscosity is zero, the fluid is frictionless and the resistance to flow is also zero. Comparing frictionless flow in a tube to viscous flow, as in Figure 12.13, we see that for a viscous fluid, speed is greatest at midstream because of drag at the boundaries. We can see the effect of viscosity in a Bunsen burner flame, even though the viscosity of natural gas is small.

The resistance  to laminar flow of an incompressible fluid having viscosity  through a horizontal tube of uniform radius  and length  , such as the one in Figure 12.14, is given by



This equation is called Poiseuille’s law for resistance after the French scientist J. L. Poiseuille (1799–1869), who derived it in an attempt to understand the flow of blood, an often turbulent fluid.

  
FIGURE 12.13 (a) If fluid flow in a tube has negligible resistance, the speed is the same all across the tube. (b) When a viscous fluid flows through a tube, its speed at the walls is zero, increasing steadily to its maximum at the center of the tube. (c) The shape of the Bunsen burner flame is due to the velocity profile across the tube. (credit: Jason Woodhead)

Let us examine Poiseuille’s expression for  to see if it makes good intuitive sense. We see that resistance is directly proportional to both fluid viscosity  and the length  of a tube. After all, both of these directly affect the amount of friction encountered—the greater either is, the greater the resistance and the smaller the flow. The radius  of a tube affects the resistance, which again makes sense, because the greater the radius, the greater the flow (all other factors remaining the same). But it is surprising that  is raised to the fourth power in Poiseuille’s law. This exponent means that any change in the radius of a tube has a very large effect on resistance. For example, doubling the radius of a tube decreases resistance by a factor of  .

Taken together,  and  give the following expression for flow rate:



This equation describes laminar flow through a tube. It is sometimes called Poiseuille’s law for laminar flow, or simply Poiseuille’s law.# EXAMPLE 12.7

# Using Flow Rate: Plaque Deposits Reduce Blood Flow

Suppose the flow rate of blood in a coronary artery has been reduced to half its normal value by plaque deposits. By what factor has the radius of the artery been reduced, assuming no turbulence occurs?

# Strategy

Assuming laminar flow, Poiseuille’s law states that



We need to compare the artery radius before and after the flow rate reduction.

# Solution

With a constant pressure difference assumed and the same length and viscosity, along the artery we have



So, given that  , we find that  .

Therefore,  , a decrease in the artery radius of 

# Discussion

This decrease in radius is surprisingly small for this situation. To restore the blood flow in spite of this buildup would require an increase in the pressure difference  of a factor of two, with subsequent strain on the heart.

TABLE 12.1 Coefficients of Viscosity of Various Fluids   

<table><tr><td rowspan=1 colspan=3>Fluid          Temperature (  Viscosity η (mPa·s)</td></tr><tr><td rowspan=1 colspan=1>Gases</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=4 colspan=1>Air</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0.0171</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0.0181</td></tr><tr><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1>0.0190</td></tr><tr><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>0.0218</td></tr><tr><td rowspan=1 colspan=1>Ammonia</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0.00974</td></tr><tr><td rowspan=1 colspan=1>Carbon dioxide</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0.0147</td></tr><tr><td rowspan=1 colspan=1>Helium</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0.0196</td></tr><tr><td rowspan=1 colspan=1>Hydrogen</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0.0090</td></tr><tr><td rowspan=1 colspan=1>Mercury</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0.0450</td></tr><tr><td rowspan=1 colspan=1>Oxygen</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0.0203</td></tr></table>TABLE 12.1 Coefficients of Viscosity of Various Fluids   

<table><tr><td rowspan=1 colspan=3>Fluid          Temperature () Viscosity  (mPa·s)</td></tr><tr><td rowspan=1 colspan=1>Steam</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>0.0130</td></tr><tr><td rowspan=1 colspan=1>Liquids</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=5 colspan=1>Water</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1.792</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>1.002</td></tr><tr><td rowspan=1 colspan=1>37</td><td rowspan=1 colspan=1>0.6947</td></tr><tr><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1>0.653</td></tr><tr><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>0.282</td></tr><tr><td rowspan=2 colspan=1>Whole blood</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>3.015</td></tr><tr><td rowspan=1 colspan=1>37</td><td rowspan=1 colspan=1>2.084</td></tr><tr><td rowspan=2 colspan=1>Blood plasma²</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>1.810</td></tr><tr><td rowspan=1 colspan=1>37</td><td rowspan=1 colspan=1>1.257</td></tr><tr><td rowspan=1 colspan=1>Ethyl alcohol</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>1.20</td></tr><tr><td rowspan=1 colspan=1>Methanol</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0.584</td></tr><tr><td rowspan=1 colspan=1>Oil (heavy machine)</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>660</td></tr><tr><td rowspan=1 colspan=1>Oil (motor, SAE 10)</td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>200</td></tr><tr><td rowspan=1 colspan=1>Oil (olive)</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>138</td></tr><tr><td rowspan=1 colspan=1>Glycerin</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>1500</td></tr><tr><td rowspan=1 colspan=1>Honey</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>2000-10000</td></tr><tr><td rowspan=1 colspan=1>Maple Syrup</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>2000-3000</td></tr><tr><td rowspan=1 colspan=1>Milk</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>3.0</td></tr><tr><td rowspan=1 colspan=1>Oil (Corn)</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>65</td></tr></table>

The circulatory system provides many examples of Poiseuille’s law in action—with blood flow regulated by changes in vessel size and blood pressure. Blood vessels are not rigid but elastic. Adjustments to blood flow are primarily made by varying the size of the vessels, since the resistance is so sensitive to the radius. During vigorous exercise, blood vessels are selectively dilated to important muscles and organs and blood pressure increases. This creates both greater overall blood flow and increased flow to specific areas. Conversely, decreases in vessel radii, perhapsfrom plaques in the arteries, can greatly reduce blood flow. If a vessel’s radius is reduced by only  (to 0.95 of its original value), the flow rate is reduced to about  of its original value. A  decrease in flow is caused by a  decrease in radius. The body may compensate by increasing blood pressure by  , but this presents hazards to the heart and any vessel that has weakened walls. Another example comes from automobile engine oil. If you have a car with an oil pressure gauge, you may notice that oil pressure is high when the engine is cold. Motor oil has greater viscosity when cold than when warm, and so pressure must be greater to pump the same amount of cold oil.

  
FIGURE 12.14 Poiseuille’s law applies to laminar flow of an incompressible fluid of viscosity  through a tube of length  and radius  . The direction of flow is from greater to lower pressure. Flow rate  is directly proportional to the pressure difference  , and inversely proportional to the length of the tube and viscosity  of the fluid. Flow rate increases with  , the fourth power of the radius.

# EXAMPLE 12.8

# What Pressure Produces This Flow Rate?

An intravenous (IV) system is supplying saline solution to a patient at the rate of  through a needle of radius  and length  . What pressure is needed at the entrance of the needle to cause this flow, assuming the viscosity of the saline solution to be the same as that of water? The gauge pressure of the blood in the patient’s vein is  . (Assume that the temperature is  .)

# Strategy

Assuming laminar flow, Poiseuille’s law applies. This is given by



where  is the pressure at the entrance of the needle and  is the pressure in the vein. The only unknown is  .

# Solution

Solving for  yields



 is given as  , which converts to  . Substituting this and the other known values yields



# Discussion

This pressure could be supplied by an IV bottle with the surface of the saline solution  above the entrance to the needle (this is left for you to solve in this chapter’s Problems and Exercises), assuming that there is negligible pressure drop in the tubing leading to the needle.# Flow and Resistance as Causes of Pressure Drops

You may have noticed that water pressure in your home might be lower than normal on hot summer days when there is more use. This pressure drop occurs in the water main before it reaches your home. Let us consider flow through the water main as illustrated in Figure 12.15. We can understand why the pressure  to the home drops during times of heavy use by rearranging



to



where, in this case,  is the pressure at the water works and  is the resistance of the water main. During times of heavy use, the flow rate  is large. This means that  must also be large. Thus  must decrease. It is correct to think of flow and resistance as causing the pressure to drop from  to  is valid for both laminar and turbulent flows.

  
FIGURE 12.15 During times of heavy use, there is a significant pressure drop in a water main, and  supplied to users is significantly less than  created at the water works. If the flow is very small, then the pressure drop is negligible, and  .

We can use  to analyze pressure drops occurring in more complex systems in which the tube radius is not the same everywhere. Resistance will be much greater in narrow places, such as an obstructed coronary artery. For a given flow rate  , the pressure drop will be greatest where the tube is most narrow. This is how water faucets control flow. Additionally,  is greatly increased by turbulence, and a constriction that creates turbulence greatly reduces the pressure downstream. Plaque in an artery reduces pressure and hence flow, both by its resistance and by the turbulence it creates.

Figure 12.16 is a schematic of the human circulatory system, showing average blood pressures in its major parts for an adult at rest. Pressure created by the heart’s two pumps, the right and left ventricles, is reduced by the resistance of the blood vessels as the blood flows through them. The left ventricle increases arterial blood pressure that drives the flow of blood through all parts of the body except the lungs. The right ventricle receives the lower pressure blood from two major veins and pumps it through the lungs for gas exchange with atmospheric gases – the disposal of carbon dioxide from the blood and the replenishment of oxygen. Only one major organ is shown schematically, with typical branching of arteries to ever smaller vessels, the smallest of which are the capillaries, and rejoining of small veins into larger ones. Similar branching takes place in a variety of organs in the body, and the circulatory system has considerable flexibility in flow regulation to these organs by the dilation and constriction of the arteries leading to them and the capillaries within them. The sensitivity of flow to tube radius makes this flexibility possible over a large range of flow rates.  
FIGURE 12.16 Schematic of the circulatory system. Pressure difference is created by the two pumps in the heart and is reduced by resistance in the vessels. Branching of vessels into capillaries allows blood to reach individual cells and exchange substances, such as oxygen and waste products, with them. The system has an impressive ability to regulate flow to individual organs, accomplished largely by varying vessel diameters.

Each branching of larger vessels into smaller vessels increases the total cross-sectional area of the tubes through which the blood flows. For example, an artery with a cross section of  may branch into 20 smaller arteries, each with cross sections of  , with a total of  . In that manner, the resistance of the branchings is reduced so that pressure is not entirely lost. Moreover, because  and  increases through branching, the average velocity of the blood in the smaller vessels is reduced. The blood velocity in the aorta (  ) is about  , while in the capillaries  in diameter) the velocity is about  . This reduced velocity allows the blood to exchange substances with the cells in the capillaries and alveoli in particular.

# 12.5 The Onset of Turbulence

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Calculate Reynolds number.   
Use the Reynolds number for a system to determine whether it is laminar or turbulent.

Sometimes we can predict if flow will be laminar or turbulent. We know that flow in a very smooth tube or around a smooth, streamlined object will be laminar at low velocity. We also know that at high velocity, even flow in a smooth tube or around a smooth object will experience turbulence. In between, it is more difficult to predict. In fact, at intermediate velocities, flow may oscillate back and forth indefinitely between laminar and turbulent.

An occlusion, or narrowing, of an artery, such as shown in Figure 12.17, is likely to cause turbulence because of the irregularity of the blockage, as well as the complexity of blood as a fluid. Turbulence in the circulatory system is noisy and can sometimes be detected with a stethoscope, such as when measuring diastolic pressure in the upper arm’s partially collapsed brachial artery. These turbulent sounds, at the onset of blood flow when the cuff pressure becomes sufficiently small, are called Korotkoff sounds. Aneurysms, or ballooning of arteries, create significant turbulence and can sometimes be detected with a stethoscope. Heart murmurs, consistent with their name, are sounds produced by turbulent flow around damaged and insufficiently closed heart valves. Ultrasound can also beused to detect turbulence as a medical indicator in a process analogous to Doppler-shift radar used to detect storms.

  
FIGURE 12.17 Flow is laminar in the large part of this blood vessel and turbulent in the part narrowed by plaque, where velocity is high. In the transition region, the flow can oscillate chaotically between laminar and turbulent flow.

An indicator called the Reynolds number  can reveal whether flow is laminar or turbulent. For flow in a tube of uniform diameter, the Reynolds number is defined as



where  is the fluid density,  its speed,  its viscosity, and  the tube radius. The Reynolds number is a unitless quantity. Experiments have revealed that  is related to the onset of turbulence. For  below about 2000, flow is laminar. For  above about 3000, flow is turbulent. For values of  between about 2000 and 3000, flow is unstable—that is, it can be laminar, but small obstructions and surface roughness can make it turbulent, and it may oscillate randomly between being laminar and turbulent. The blood flow through most of the body is a quiet, laminar flow. The exception is in the aorta, where the speed of the blood flow rises above a critical value of  and becomes turbulent.

# EXAMPLE 12.9

# Is This Flow Laminar or Turbulent?

Calculate the Reynolds number for flow in the needle considered in Example 12.8 to verify the assumption that the flow is laminar. Assume that the density of the saline solution is  .

# Strategy

We have all of the information needed, except the fluid speed  , which can be calculated from  (verification of this is in this chapter’s Problems and Exercises).

# Solution

Entering the known values into  gives



# Discussion

Since  is well below 2000, the flow should indeed be laminar.# Take-Home Experiment: Inhalation

Under the conditions of normal activity, an adult inhales about 1 L of air during each inhalation. With the aid of a watch, determine the time for one of your own inhalations by timing several breaths and dividing the total length by the number of breaths. Calculate the average flow rate  of air traveling through the trachea during each inhalation.

The topic of chaos has become quite popular over the last few decades. A system is defined to be chaotic when its behavior is so sensitive to some factor that it is extremely difficult to predict. The field of chaos is the study of chaotic behavior. A good example of chaotic behavior is the flow of a fluid with a Reynolds number between 2000 and 3000. Whether or not the flow is turbulent is difficult, but not impossible, to predict—the difficulty lies in the extremely sensitive dependence on factors like roughness and obstructions on the nature of the flow. A tiny variation in one factor has an exaggerated (or nonlinear) effect on the flow. Phenomena as disparate as turbulence, the orbit of Pluto, and the onset of irregular heartbeats are chaotic and can be analyzed with similar techniques.

# 12.6 Motion of an Object in a Viscous Fluid

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Calculate the Reynolds number for an object moving through a fluid.   
Explain whether the Reynolds number indicates laminar or turbulent flow.   
Describe the conditions under which an object has a terminal speed.

A moving object in a viscous fluid is equivalent to a stationary object in a flowing fluid stream. (For example, when you ride a bicycle at  in still air, you feel the air in your face exactly as if you were stationary in a  wind.) Flow of the stationary fluid around a moving object may be laminar, turbulent, or a combination of the two. Just as with flow in tubes, it is possible to predict when a moving object creates turbulence. We use another form of the Reynolds number  , defined for an object moving in a fluid to be



where  is a characteristic length of the object (a sphere’s diameter, for example),  the fluid density,  its viscosity, and  the object’s speed in the fluid. If  is less than about 1, flow around the object can be laminar, particularly if the object has a smooth shape. The transition to turbulent flow occurs for  between 1 and about 10, depending on surface roughness and so on. Depending on the surface, there can be a turbulent wake behind the object with some laminar flow over its surface. For an  between 10 and  , the flow may be either laminar or turbulent and may oscillate between the two. For  greater than about  , the flow is entirely turbulent, even at the surface of the object. (See Figure 12.18.) Laminar flow occurs mostly when the objects in the fluid are small, such as raindrops, pollen, and blood cells in plasma.

# EXAMPLE 12.10

# Does a Ball Have a Turbulent Wake?

Calculate the Reynolds number  for a ball with a 7.40-cm diameter thrown at  .

# Strategy

We can use  to calculate  , since all values in it are either given or can be found in tables of density and viscosity.

# Solution

Substituting values into the equation for  yields

# Discussion

This value is sufficiently high to imply a turbulent wake. Most large objects, such as airplanes and sailboats, create significant turbulence as they move. As noted before, the Bernoulli principle gives only qualitatively-correct results in such situations.

One of the consequences of viscosity is a resistance force called viscous drag  that is exerted on a moving object. This force typically depends on the object’s speed (in contrast with simple friction). Experiments have shown that for laminar flow (  less than about one) viscous drag is proportional to speed, whereas for  between about 10 and  , viscous drag is proportional to speed squared. (This relationship is a strong dependence and is pertinent to bicycle racing, where even a small headwind causes significantly increased drag on the racer. Cyclists take turns being the leader in the pack for this reason.) For  greater than  , drag increases dramatically and behaves with greater complexity. For laminar flow around a sphere,  is proportional to fluid viscosity  , the object’s characteristic size  , and its speed  . All of which makes sense—the more viscous the fluid and the larger the object, the more drag we expect. Recall Stoke’s law  . For the special case of a small sphere of radius  moving slowly in a fluid of viscosity  , the drag force  is given by



  
FIGURE 12.18 (a) Motion of this sphere to the right is equivalent to fluid flow to the left. Here the flow is laminar with  less than 1. There is a force, called viscous drag  , to the left on the ball due to the fluid’s viscosity. (b) At a higher speed, the flow becomes partially turbulent, creating a wake starting where the flow lines separate from the surface. Pressure in the wake is less than in front of the sphere, because fluid speed is less, creating a net force to the left  that is significantly greater than for laminar flow. Here  is greater than 10. (c) At much higher speeds, where  is greater than  , flow becomes turbulent everywhere on the surface and behind the sphere. Drag increases dramatically.

An interesting consequence of the increase in  with speed is that an object falling through a fluid will not continue to accelerate indefinitely (as it would if we neglect air resistance, for example). Instead, viscous drag increases, slowing acceleration, until a critical speed, called the terminal speed, is reached and the acceleration of the object becomes zero. Once this happens, the object continues to fall at constant speed (the terminal speed). This is the case for particles of sand falling in the ocean, cells falling in a centrifuge, and sky divers falling through the air. Figure 12.19 shows some of the factors that affect terminal speed. There is a viscous drag on the object that depends on the viscosity of the fluid and the size of the object. But there is also a buoyant force that depends on the density of the object relative to the fluid. Terminal speed will be greatest for low-viscosity fluids and objects with high densities and small sizes. Thus a skydiver falls more slowly with outspread limbs than when they are in a pike position—head first with hands at their side and legs together.

# Take-Home Experiment: Don’t Lose Your Marbles

By measuring the terminal speed of a slowly moving sphere in a viscous fluid, one can find the viscosity of that fluid (at that temperature). It can be difficult to find small ball bearings around the house, but a small marble will do. Gather two or three fluids (syrup, motor oil, honey, olive oil, etc.) and a thick, tall clear glass or vase. Drop the marble into the center of the fluid and time its fall (after letting it drop a little to reach its terminal speed).Compare your values for the terminal speed and see if they are inversely proportional to the viscosities as listed in Table 12.1. Does it make a difference if the marble is dropped near the side of the glass?

Knowledge of terminal speed is useful for estimating sedimentation rates of small particles. We know from watching mud settle out of dirty water that sedimentation is usually a slow process. Centrifuges are used to speed sedimentation by creating accelerated frames in which gravitational acceleration is replaced by centripetal acceleration, which can be much greater, increasing the terminal speed.

  
FIGURE 12.19 There are three forces acting on an object falling through a viscous fluid: its weight  , the viscous drag  , and the buoyant force  .

12.7 Molecular Transport Phenomena: Diffusion, Osmosis, and Related Processes

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Define diffusion, osmosis, dialysis, and active transport.   
Calculate diffusion rates.

# Diffusion

There is something fishy about the ice cube from your freezer—how did it pick up those food odors? How does soaking a sprained ankle in Epsom salt reduce swelling? The answer to these questions are related to atomic and molecular transport phenomena—another mode of fluid motion. Atoms and molecules are in constant motion at any temperature. In fluids they move about randomly even in the absence of macroscopic flow. This motion is called a random walk and is illustrated in Figure 12.20. Diffusion is the movement of substances due to random thermal molecular motion. Fluids, like fish fumes or odors entering ice cubes, can even diffuse through solids.

Diffusion is a slow process over macroscopic distances. The densities of common materials are great enough that molecules cannot travel very far before having a collision that can scatter them in any direction, including straight backward. It can be shown that the average distance  that a molecule travels is proportional to the square root of time:



where  stands for the root-mean-square distance and is the statistical average for the process. The quantity  is the diffusion constant for the particular molecule in a specific medium. Table 12.2 lists representative values of  for various substances, in units of  .  
FIGURE 12.20 The random thermal motion of a molecule in a fluid in time  . This type of motion is called a random walk.

TABLE 12.2 Diffusion Constants for Various Molecules3   

<table><tr><td rowspan=1 colspan=3>Diffusing molecule  Medium   D (m²½/s)</td></tr><tr><td rowspan=1 colspan=1>Hydrogen (H2)</td><td rowspan=1 colspan=1>Air</td><td rowspan=1 colspan=1>6.4 × 10-5</td></tr><tr><td rowspan=1 colspan=1>Oxygen (02)</td><td rowspan=1 colspan=1>Air</td><td rowspan=1 colspan=1>1.8 × 10-5</td></tr><tr><td rowspan=1 colspan=1>Oxygen (O2)</td><td rowspan=1 colspan=1>Water</td><td rowspan=1 colspan=1>1.0 × 10-9</td></tr><tr><td rowspan=1 colspan=1>Glucose (C6H1206)</td><td rowspan=1 colspan=1>Water</td><td rowspan=1 colspan=1>6.7 × 10-10</td></tr><tr><td rowspan=1 colspan=1>Hemoglobin</td><td rowspan=1 colspan=1>Water</td><td rowspan=1 colspan=1>6.9 × 10-11</td></tr><tr><td rowspan=1 colspan=1>DNA</td><td rowspan=1 colspan=1>Water</td><td rowspan=1 colspan=1>1.3 × 10−12</td></tr></table>

Note that  gets progressively smaller for more massive molecules. This decrease is because the average molecular speed at a given temperature is inversely proportional to molecular mass. Thus the more massive molecules diffuse more slowly. Another interesting point is that  for oxygen in air is much greater than  for oxygen in water. In water, an oxygen molecule makes many more collisions in its random walk and is slowed considerably. In water, an oxygen molecule moves only about  in 1 s. (Each molecule actually collides about  times per second!). Finally, note that diffusion constants increase with temperature, because average molecular speed increases with temperature. This is because the average kinetic energy of molecules,  , is proportional to absolute temperature.

# EXAMPLE 12.11

# Calculating Diffusion: How Long Does Glucose Diffusion Take?

Calculate the average time it takes a glucose molecule to move  in water.# Strategy

We can use  , the expression for the average distance moved in time  , and solve it for . All other quantities are known.

# Solution

Solving for  and substituting known values yields



# Discussion

This is a remarkably long time for glucose to move a mere centimeter! For this reason, we stir sugar into water rather than waiting for it to diffuse.

Because diffusion is typically very slow, its most important effects occur over small distances. For example, the cornea of the eye gets most of its oxygen by diffusion through the thin tear layer covering it.

# The Rate and Direction of Diffusion

If you very carefully place a drop of food coloring in a still glass of water, it will slowly diffuse into the colorless surroundings until its concentration is the same everywhere. This type of diffusion is called free diffusion, because there are no barriers inhibiting it. Let us examine its direction and rate. Molecular motion is random in direction, and so simple chance dictates that more molecules will move out of a region of high concentration than into it. The net rate of diffusion is higher initially than after the process is partially completed. (See Figure 12.21.)

  
FIGURE 12.21 Diffusion proceeds from a region of higher concentration to a lower one. The net rate of movement is proportional to the difference in concentration.

The net rate of diffusion is proportional to the concentration difference. Many more molecules will leave a region of high concentration than will enter it from a region of low concentration. In fact, if the concentrations were the same, there would be no net movement. The net rate of diffusion is also proportional to the diffusion constant  , which is determined experimentally. The farther a molecule can diffuse in a given time, the more likely it is to leave the region of high concentration. Many of the factors that affect the rate are hidden in the diffusion constant  . For example, temperature and cohesive and adhesive forces all affect values of  .

Diffusion is the dominant mechanism by which the exchange of nutrients and waste products occur between the blood and tissue, and between air and blood in the lungs. In the evolutionary process, as organisms became larger, they needed quicker methods of transportation than net diffusion, because of the larger distances involved in the transport, leading to the development of circulatory systems. Less sophisticated, single-celled organisms still rely totally on diffusion for the removal of waste products and the uptake of nutrients.# Osmosis and Dialysis—Diffusion across Membranes

Some of the most interesting examples of diffusion occur through barriers that affect the rates of diffusion. For example, when you soak a swollen ankle in Epsom salt, water diffuses through your skin. Many substances regularly move through cell membranes; oxygen moves in, carbon dioxide moves out, nutrients go in, and wastes go out, for example. Because membranes are thin structures (typically  to  m across) diffusion rates through them can be high. Diffusion through membranes is an important method of transport.

Membranes are generally selectively permeable, or semipermeable. (See Figure 12.22.) One type of semipermeable membrane has small pores that allow only small molecules to pass through. In other types of membranes, the molecules may actually dissolve in the membrane or react with molecules in the membrane while moving across. Membrane function, in fact, is the subject of much current research, involving not only physiology but also chemistry and physics.

  
FIGURE 12.22 (a) A semipermeable membrane with small pores that allow only small molecules to pass through. (b) Certain molecules dissolve in this membrane and diffuse across it.

Osmosis is the transport of water through a semipermeable membrane from a region of high concentration to a region of low concentration. Osmosis is driven by the imbalance in water concentration. For example, water is more concentrated in your body than in Epsom salt. When you soak a swollen ankle in Epsom salt, the water moves out of your body into the lower-concentration region in the salt. Similarly, dialysis is the transport of any other molecule through a semipermeable membrane due to its concentration difference. Both osmosis and dialysis are used by the kidneys to cleanse the blood.

Osmosis can create a substantial pressure. Consider what happens if osmosis continues for some time, as illustrated in Figure 12.23. Water moves by osmosis from the left into the region on the right, where it is less concentrated, causing the solution on the right to rise. This movement will continue until the pressure created by the extra height of fluid on the right is large enough to stop further osmosis. This pressure is called a back pressure. The back pressure  that stops osmosis is also called the relative osmotic pressure if neither solution is pure water, and it is called the osmotic pressure if one solution is pure water. Osmotic pressure can be large, depending on the size of the concentration difference. For example, if pure water and sea water are separated by a semipermeable membrane that passes no salt, osmotic pressure will be 25.9 atm. This value means that water will diffuse through the membrane until the salt water surface rises  above the pure-water surface! One example of pressure created by osmosis is turgor in plants (many wilt when too dry). Turgor describes the condition of a plant in which the fluid in a cell exerts a pressure against the cell wall. This pressure gives the plant support. Dialysis can similarly cause substantial pressures.  
FIGURE 12.23 (a) Two sugar-water solutions of different concentrations, separated by a semipermeable membrane that passes water but not sugar. Osmosis will be to the right, since water is less concentrated there. (b) The fluid level rises until the back pressure equals the relative osmotic pressure; then, the net transfer of water is zero.

Reverse osmosis and reverse dialysis (also called filtration) are processes that occur when back pressure is sufficient to reverse the normal direction of substances through membranes. Back pressure can be created naturally as on the right side of Figure 12.23. (A piston can also create this pressure.) Reverse osmosis can be used to desalinate water by simply forcing it through a membrane that will not pass salt. Similarly, reverse dialysis can be used to filter out any substance that a given membrane will not pass.

One further example of the movement of substances through membranes deserves mention. We sometimes find that substances pass in the direction opposite to what we expect. Cypress tree roots, for example, extract pure water from salt water, although osmosis would move it in the opposite direction. This is not reverse osmosis, because there is no back pressure to cause it. What is happening is called active transport, a process in which a living membrane expends energy to move substances across it. Many living membranes move water and other substances by active transport. The kidneys, for example, not only use osmosis and dialysis—they also employ significant active transport to move substances into and out of blood. In fact, it is estimated that at least  of the body’s energy is expended on active transport of substances at the cellular level. The study of active transport carries us into the realms of microbiology, biophysics, and biochemistry and it is a fascinating application of the laws of nature to living structures.# Glossary

active transport the process in which a living membrane expends energy to move substances across   
Bernoulli’s equation the equation resulting from applying conservation of energy to an incompressible frictionless fluid:  constant , through the fluid   
Bernoulli’s principle Bernoulli’s equation applied at constant depth:    
dialysis the transport of any molecule other than water through a semipermeable membrane from a region of high concentration to one of low concentration   
diffusion the movement of substances due to random thermal molecular motion   
flow rate abbreviated  it is the volume V that flows past a particular point during a time t, or    
fluid dynamics the physics of fluids in motion   
laminar a type of fluid flow in which layers do not mix   
liter a unit of volume, equal to    
osmosis the transport of water through a semipermeable membrane from a region of high concentration to one of low concentration   
osmotic pressure the back pressure which stops the osmotic process if one solution is pure water   
Poiseuille’s law the rate of laminar flow of an incompressible fluid in a tube:    
Poiseuille’s law for resistance the resistance to laminar flow of an incompressible fluid in a tube:     
relative osmotic pressure the back pressure which stops the osmotic process if neither solution is pure water   
reverse dialysis the process that occurs when back pressure is sufficient to reverse the normal direction of dialysis through membranes   
reverse osmosis the process that occurs when back pressure is sufficient to reverse the normal direction of osmosis through membranes   
Reynolds number a dimensionless parameter that can reveal whether a particular flow is laminar or turbulent   
semipermeable a type of membrane that allows only certain small molecules to pass through   
terminal speed the speed at which the viscous drag of an object falling in a viscous fluid is equal to the other forces acting on the object (such as gravity), so that the acceleration of the object is zero   
turbulence fluid flow in which layers mix together via eddies and swirls   
viscosity the friction in a fluid, defined in terms of the friction between layers   
viscous drag a resistance force exerted on a moving object, with a nontrivial dependence on velocity

# Section Summary

# 12.1 Flow Rate and Its Relation to Velocity

• Flow rate  is defined to be the volume  flowing past a point in time  , or  where  is volume and  is time.   
The SI unit of volume is  . Another common unit is the liter (L), which is  . Flow rate and velocity are related by  where  is the cross-sectional area of the flow and  is its average velocity. For incompressible fluids, flow rate at various points is constant. That is, 

# 12.2 Bernoulli’s Equation

• Bernoulli’s equation states that the sum on each side of the following equation is constant, or the same at any two points in an incompressible frictionless fluid:

   
Bernoulli’s principle is Bernoulli’s equation applied to situations in which depth is constant. The terms involving depth (or height  ) subtract out, yielding    
Bernoulli’s principle has many applications,   
including entrainment, wings and sails, and   
velocity measurement.

# 12.3 The Most General Applications of Bernoulli’s Equation

• Power in fluid flow is given by the equation  where the first term is power associated with pressure, the second is power associated with velocity, and the third is power associated with height.

# 12.4 Viscosity and Laminar Flow; Poiseuille’s Law

• Laminar flow is characterized by smooth flow ofthe fluid in layers that do not mix.   
• Turbulence is characterized by eddies and swirls that mix layers of fluid together.   
Fluid viscosity  is due to friction within a fluid. Representative values are given in Table 12.1. Viscosity has units of  or  . Flow is proportional to pressure difference and inversely proportional to resistance:    
• For laminar flow in a tube, Poiseuille’s law for resistance states that  Poiseuille’s law for flow in a tube is  The pressure drop caused by flow and resistance is given by 

# 12.5 The Onset of Turbulence

• The Reynolds number  can reveal whether flow is laminar or turbulent. It is    
For  below about 2000, flow is laminar. For  above about 3000, flow is turbulent. For values of  between 2000 and 3000, it may be either or both.

# 12.6 Motion of an Object in a Viscous Fluid

• When an object moves in a fluid, there is a different form of the Reynolds number  which indicates whether flow is laminar or turbulent. • For  less than about one, flow is laminar. • For  greater than  , flow is entirely turbulent.

# 12.7 Molecular Transport Phenomena: Diffusion, Osmosis, and Related Processes

• Diffusion is the movement of substances due to random thermal molecular motion. The average distance  a molecule travels by diffusion in a given amount of time is given by  where  is the diffusion constant, representative values of which are found in Table 12.2. Osmosis is the transport of water through a semipermeable membrane from a region of high concentration to a region of low concentration. Dialysis is the transport of any other molecule through a semipermeable membrane due to its concentration difference. Both processes can be reversed by back pressure. Active transport is a process in which a living membrane expends energy to move substances across it.

# Conceptual Questions

# 12.1 Flow Rate and Its Relation to Velocity

1. What is the difference between flow rate and fluid velocity? How are they related?   
2. Many figures in the text show streamlines. Explain why fluid velocity is greatest where streamlines are closest together. (Hint: Consider the relationship between fluid velocity and the cross-sectional area through which it flows.)   
3. Identify some substances that are incompressible and some that are not.

# 12.2 Bernoulli’s Equation

4. You can squirt water a considerably greater distance by placing your thumb over the end of a garden hose and then releasing, than by leaving it completely uncovered. Explain how this works.

5. Water is shot nearly vertically upward in a decorative fountain and the stream is observed to broaden as it rises. Conversely, a stream of water falling straight down from a faucet narrows. Explain why, and discuss whether surface tension enhances or reduces the effect in each case.   
6. Look back to Figure 12.4. Answer the following two questions. Why is  less than atmospheric? Why is  greater than    
7. Give an example of entrainment not mentioned in the text.   
8. Many entrainment devices have a constriction, called a Venturi, such as shown in Figure 12.24. How does this bolster entrainment?  
FIGURE 12.24 A tube with a narrow segment designed to enhance entrainment is called a Venturi. These are very commonly used in carburetors and aspirators.

9. Some chimney pipes have a T-shape, with a crosspiece on top that helps draw up gases whenever there is even a slight breeze. Explain how this works in terms of Bernoulli’s principle.   
10. Is there a limit to the height to which an entrainment device can raise a fluid? Explain your answer.   
11. Why is it preferable for airplanes to take off into the wind rather than with the wind?   
12. Roofs are sometimes pushed off vertically during a tropical cyclone, and buildings sometimes explode outward when hit by a tornado. Use Bernoulli’s principle to explain these phenomena.   
13. Why does a sailboat need a keel?   
14. It is dangerous to stand close to railroad tracks when a rapidly moving commuter train passes. Explain why atmospheric pressure would push you toward the moving train.   
15. Water pressure inside a hose nozzle can be less than atmospheric pressure due to the Bernoulli effect. Explain in terms of energy how the water can emerge from the nozzle against the opposing atmospheric pressure.

16. A perfume bottle or atomizer sprays a fluid that is in the bottle. (Figure 12.25.) How does the fluid rise up in the vertical tube in the bottle?

  
FIGURE 12.25 Atomizer: perfume bottle with tube to carry perfume up through the bottle. (credit: Antonia Foy, Flickr)

17. If you lower the window on a car while moving, an empty plastic bag can sometimes fly out the window. Why does this happen?

# 12.3 The Most General Applications of Bernoulli’s Equation

18. Based on Bernoulli’s equation, what are three forms of energy in a fluid? (Note that these forms are conservative, unlike heat transfer and other dissipative forms not included in Bernoulli’s equation.)   
19. Water that has emerged from a hose into the atmosphere has a gauge pressure of zero. Why? When you put your hand in front of the emerging stream you feel a force, yet the water’s gauge pressure is zero. Explain where the force comes from in terms of energy.20. The old rubber boot shown in Figure 12.26 has two leaks. To what maximum height can the water squirt from Leak 1? How does the velocity of water emerging from Leak 2 differ from that of leak 1? Explain your responses in terms of energy.

  
FIGURE 12.26 Water emerges from two leaks in an old boot.

21. Water pressure inside a hose nozzle can be less than atmospheric pressure due to the Bernoulli effect. Explain in terms of energy how the water can emerge from the nozzle against the opposing atmospheric pressure.

# 12.4 Viscosity and Laminar Flow; Poiseuille’s Law

22. Explain why the viscosity of a liquid decreases with temperature—that is, how might increased temperature reduce the effects of cohesive forces in a liquid? Also explain why the viscosity of a gas increases with temperature—that is, how does increased gas temperature create more collisions between atoms and molecules?

23. When paddling a canoe upstream, it is wisest to travel as near to the shore as possible. When canoeing downstream, it may be best to stay near the middle. Explain why.

24. Why does flow decrease in your shower when someone flushes the toilet?

25. Plumbing usually includes air-filled tubes near water faucets, as shown in Figure 12.27. Explain why they are needed and how they work.

  
FIGURE 12.27 The vertical tube near the water tap remains full of air and serves a useful purpose.

# 12.5 The Onset of Turbulence

26. Doppler ultrasound can be used to measure the speed of blood in the body. If there is a partial constriction of an artery, where would you expect blood speed to be greatest, at or nearby the constriction? What are the two distinct causes of higher resistance in the constriction?

27. Sink drains often have a device such as that shown in Figure 12.28 to help speed the flow of water. How does this work?

  
FIGURE 12.28 You will find devices such as this in many drains. They significantly increase flow rate.

28. Some ceiling fans have decorative wicker reeds on their blades. Discuss whether these fans are as quiet and efficient as those with smooth blades.

# 12.6 Motion of an Object in a Viscous Fluid

29. What direction will a helium balloon move inside a car that is slowing down—toward the front or back? Explain your answer.30. Will identical raindrops fall more rapidly in  air or  air, neglecting any differences in air density? Explain your answer.

31. If you took two marbles of different sizes, what would you expect to observe about the relative magnitudes of their terminal velocities?

# 12.7 Molecular Transport Phenomena: Diffusion, Osmosis, and Related Processes

32. Why would you expect the rate of diffusion to increase with temperature? Can you give an example, such as the fact that you can dissolve sugar more rapidly in hot water?

33. How are osmosis and dialysis similar? How do they differ?

# Problems & Exercises

# 12.1 Flow Rate and Its Relation to Velocity

1. What is the average flow rate in  of gasoline to the engine of a car traveling at  if it averages 

2. The heart of a resting adult pumps blood at a rate of  . (a) Convert this to  . (b) What is this rate in 

3. Blood is pumped from the heart at a rate of  min into the aorta (of radius  ). Determine the speed of blood through the aorta.

4. Blood is flowing through an artery of radius  at a rate of  . Determine the flow rate and the volume that passes through the artery in a period of  .

5. The Huka Falls on the Waikato River is one of New Zealand’s most visited natural tourist attractions (see Figure 12.29). On average the river has a flow rate of about  . At the gorge, the river narrows to  wide and averages  deep. (a) What is the average speed of the river in the gorge? (b) What is the average speed of the water in the river downstream of the falls when it widens to 60 m and its depth increases to an average of 

  
FIGURE 12.29 The Huka Falls in Taupo, New Zealand, demonstrate flow rate. (credit: RaviGogna, Flickr)

6. A major artery with a cross-sectional area of  branches into 18 smaller arteries, each with an average cross-sectional area of  By what factor is the average velocity of the blood reduced when it passes into these branches?

7. (a) As blood passes through the capillary bed in an organ, the capillaries join to form venules (small veins). If the blood speed increases by a factor of 4.00 and the total cross-sectional area of the venules is  , what is the total crosssectional area of the capillaries feeding these venules? (b) How many capillaries are involved if their average diameter is 

8. The human circulation system has approximately  capillary vessels. Each vessel has a diameter of about  . Assuming cardiac output is  , determine the average velocity of blood flow through each capillary vessel.

9. (a) Estimate the time it would take to fill a private swimming pool with a capacity of 80,000 L using a garden hose delivering  . (b) How long would it take to fill if you could divert a moderate size river, flowing at  , into it?

10. The flow rate of blood through a  -m -radius capillary is  (a) What is the speed of the blood flow? (This small speed allows time for diffusion of materials to and from the blood.) (b) Assuming all the blood in the body passes through capillaries, how many of them must there be to carry a total flow of  (The large number obtained is an overestimate, but it is still reasonable.)

11. (a) What is the fluid speed in a fire hose with a 9.00-cm diameter carrying 80.0 L of water per second? (b) What is the flow rate in cubic meters per second? (c) Would your answers be different if salt water replaced the fresh water in the fire hose?

12. The main uptake air duct of a forced air gas heater is  in diameter. What is the average speed of air in the duct if it carries a volume equal to that of the house’s interior every 15 min? The inside volume of the house is equivalent to a rectangular solid  wide by  long by  high.13. Water is moving at a velocity of  through a hose with an internal diameter of  . (a) What is the flow rate in liters per second? (b) The fluid velocity in this hose’s nozzle is  . What is the nozzle’s inside diameter?

14. Prove that the speed of an incompressible fluid through a constriction, such as in a Venturi tube, increases by a factor equal to the square of the factor by which the diameter decreases. (The converse applies for flow out of a constriction into a larger-diameter region.)

15. Water emerges straight down from a faucet with a 1.80-cm diameter at a speed of  . (Because of the construction of the faucet, there is no variation in speed across the stream.) (a) What is the flow rate in  (b) What is the diameter of the stream  below the faucet? Neglect any effects due to surface tension.

16. Unreasonable Results A mountain stream is  wide and averages  in depth. During the spring runoff, the flow in the stream reaches  (a) What is the average velocity of the stream under these conditions? (b) What is unreasonable about this velocity? (c) What is unreasonable or inconsistent about the premises?

# 12.2 Bernoulli’s Equation

17. Verify that pressure has units of energy per unit volume.

18. Suppose you have a wind speed gauge like the pitot tube shown in Example 12.2(b). By what factor must wind speed increase to double the value of  in the manometer? Is this independent of the moving fluid and the fluid in the manometer?

19. If the pressure reading of your pitot tube is 15.0 mm  at a speed of  , what will it be at  at the same altitude?

20. Calculate the maximum height to which water could be squirted with the hose in Example 12.2 example if it: (a) Emerges from the nozzle. (b) Emerges with the nozzle removed, assuming the same flow rate.

21. Every few years, winds in Boulder, Colorado, attain sustained speeds of  (about  ) when the jet stream descends during early spring. Approximately what is the force due to the Bernoulli effect on a roof having an area of  Typical air density in Boulder is  , and the corresponding atmospheric pressure is  . (Bernoulli’s principle as stated in the text assumes laminar flow. Using the principle here produces only an approximate result, because there is significant turbulence.)

22. (a) Calculate the approximate force on a square meter of sail, given the horizontal velocity of the wind is  parallel to its front surface and  along its back surface. Take the density of air to be  . (The calculation, based on Bernoulli’s principle, is approximate due to the effects of turbulence.) (b) Discuss whether this force is great enough to be effective for propelling a sailboat.

23. (a) What is the pressure drop due to the Bernoulli effect as water goes into a 3.00-cm-diameter nozzle from a 9.00-cm-diameter fire hose while carrying a flow of  (b) To what maximum height above the nozzle can this water rise? (The actual height will be significantly smaller due to air resistance.)

24. (a) Using Bernoulli’s equation, show that the measured fluid speed  for a pitot tube, like the one in Figure 12.7(b), is given by  where  is the height of the manometer fluid,  is the density of the manometer fluid,  is the density of the moving fluid, and  is the acceleration due to gravity. (Note that  is indeed proportional to the square root of  , as stated in the text.) (b) Calculate  for moving air if a mercury manometer’s  is  .

# 12.3 The Most General Applications of Bernoulli’s Equation

25. Hoover Dam on the Colorado River is the highest dam in the United States at  , with an output of 1300 MW. The dam generates electricity with water taken from a depth of  and an average flow rate of  . (a) Calculate the power in this flow. (b) What is the ratio of this power to the facility’s average of 680 MW?26. A frequently quoted rule of thumb in aircraft design is that wings should produce about 1000 N of lift per square meter of wing. (The fact that a wing has a top and bottom surface does not double its area.) (a) At takeoff, an aircraft travels at  , so that the air speed relative to the bottom of the wing is  . Given the sea level density of air to be  , how fast must it move over the upper surface to create the ideal lift? (b) How fast must air move over the upper surface at a cruising speed of  and at an altitude where air density is one-fourth that at sea level? (Note that this is not all of the aircraft’s lift—some comes from the body of the plane, some from engine thrust, and so on. Furthermore, Bernoulli’s principle gives an approximate answer because flow over the wing creates turbulence.)

27. The left ventricle of a resting adult’s heart pumps blood at a flow rate of  , increasing its pressure by  , its speed from zero to  , and its height by  . (All numbers are averaged over the entire heartbeat.) Calculate the total power output of the left ventricle. Note that most of the power is used to increase blood pressure.

28. A sump pump (used to drain water from the basement of houses built below the water table) is draining a flooded basement at the rate of 0.750  , with an output pressure of  . (a) The water enters a hose with a 3.00-cm inside diameter and rises  above the pump. What is its pressure at this point? (b) The hose goes over the foundation wall, losing  in height, and widens to  in diameter. What is the pressure now? You may neglect frictional losses in both parts of the problem.

# 12.4 Viscosity and Laminar Flow; Poiseuille’s Law

29. (a) Calculate the retarding force due to the viscosity of the air layer between a cart and a level air track given the following information—air temperature is  , the cart is moving at 0.400  , its surface area is  , and the thickness of the air layer is  . (b) What is the ratio of this force to the weight of the 0.300-kg cart?

30. What force is needed to pull one microscope slide over another at a speed of  , if there is a  -thick layer of  water between them and the contact area is 

31. A glucose solution being administered with an IV has a flow rate of  . What will the new flow rate be if the glucose is replaced by whole blood having the same density but a viscosity 2.50 times that of the glucose? All other factors remain constant.

32. The pressure drop along a length of artery is 100 Pa, the radius is  , and the flow is laminar. The average speed of the blood is  . (a) What is the net force on the blood in this section of artery? (b) What is the power expended maintaining the flow?

33. A small artery has a length of  and a radius of  . If the pressure drop across the artery is  , what is the flow rate through the artery? (Assume that the temperature is  .)

34. Fluid originally flows through a tube at a rate of  . To illustrate the sensitivity of flow rate to various factors, calculate the new flow rate for the following changes with all other factors remaining the same as in the original conditions. (a) Pressure difference increases by a factor of 1.50. (b) A new fluid with 3.00 times greater viscosity is substituted. (c) The tube is replaced by one having 4.00 times the length. (d) Another tube is used with a radius 0.100 times the original. (e) Yet another tube is substituted with a radius 0.100 times the original and half the length, and the pressure difference is increased by a factor of 1.50.

35. The arterioles (small arteries) leading to an organ, constrict in order to decrease flow to the organ. To shut down an organ, blood flow is reduced naturally to  of its original value. By what factor did the radii of the arterioles constrict? Penguins do this when they stand on ice to reduce the blood flow to their feet.

36. Angioplasty is a technique in which arteries partially blocked with plaque are dilated to increase blood flow. By what factor must the radius of an artery be increased in order to increase blood flow by a factor of 10?

37. (a) Suppose a blood vessel’s radius is decreased to  of its original value by plaque deposits and the body compensates by increasing the pressure difference along the vessel to keep the flow rate constant. By what factor must the pressure difference increase? (b) If turbulence is created by the obstruction, what additional effect would it have on the flow rate?38. A spherical particle falling at a terminal speed in a liquid must have the gravitational force balanced by the drag force and the buoyant force. The buoyant force is equal to the weight of the displaced fluid, while the drag force is assumed to be given by Stokes Law,  . Show that the terminal speed is given by  where  is the radius of the sphere,  is its density, and  is the density of the fluid and  the coefficient of viscosity.

39. Using the equation of the previous problem, find the viscosity of motor oil in which a steel ball of radius  falls with a terminal speed of 4.32  . The densities of the ball and the oil are 7.86 and  , respectively.

40. A skydiver will reach a terminal velocity when the air drag equals their weight. For a skydiver with high speed and a large body, turbulence is a factor. The drag force then is approximately proportional to the square of the velocity. Taking the drag force to be  and setting this equal to the person’s weight, find the terminal speed for a person falling “spread eagle.” Find both a formula and a number for  , with assumptions as to size.

41. A layer of oil  thick is placed between two microscope slides. Researchers find that a force of  is required to glide one over the other at a speed of  when their contact area is  . What is the oil’s viscosity? What type of oil might it be?

42. (a) Verify that a  decrease in laminar flow through a tube is caused by a  decrease in radius, assuming that all other factors remain constant, as stated in the text. (b) What increase in flow is obtained from a  increase in radius, again assuming all other factors remain constant?

43. Example 12.8 dealt with the flow of saline solution in an IV system. (a) Verify that a pressure of  is created at a depth of  in a saline solution, assuming its density to be that of sea water. (b) Calculate the new flow rate if the height of the saline solution is decreased to 1.50 m. (c) At what height would the direction of flow be reversed? (This reversal can be a problem when patients stand up.)

44. When physicians diagnose arterial blockages, they quote the reduction in flow rate. If the flow rate in an artery has been reduced to  of its normal value by a blood clot and the average pressure difference has increased by  , by what factor has the clot reduced the radius of the artery?

45. During a marathon race, a runner’s blood flow increases to 10.0 times her resting rate. Her blood’s viscosity has dropped to  of its normal value, and the blood pressure difference across the circulatory system has increased by  . By what factor has the average radii of her blood vessels increased?

46. Water supplied to a house by a water main has a pressure of  early on a summer day when neighborhood use is low. This pressure produces a flow of  through a garden hose. Later in the day, pressure at the exit of the water main and entrance to the house drops, and a flow of only  is obtained through the same hose. (a) What pressure is now being supplied to the house, assuming resistance is constant? (b) By what factor did the flow rate in the water main increase in order to cause this decrease in delivered pressure? The pressure at the entrance of the water main is  , and the original flow rate was  (c) How many more users are there, assuming each would consume  in the morning?

47. An oil gusher shoots crude oil  into the air through a pipe with a  diameter. Neglecting air resistance but not the resistance of the pipe, and assuming laminar flow, calculate the gauge pressure at the entrance of the  -long vertical pipe. Take the density of the oil to be  and its viscosity to be  (or  ). Note that you must take into account the pressure due to the  column of oil in the pipe.

48. Concrete is pumped from a cement mixer to the place it is being laid, instead of being carried in wheelbarrows. The flow rate is  through a 50.0-m-long, 8.00-cm-diameter hose, and the pressure at the pump is  . (a) Calculate the resistance of the hose. (b) What is the viscosity of the concrete, assuming the flow is laminar? (c) How much power is being supplied, assuming the point of use is at the same level as the pump? You may neglect the power supplied to increase the concrete’s velocity.

49. Construct Your Own Problem Consider a coronary artery constricted by arteriosclerosis. Construct a problem in which you calculate the amount by which the diameter of the artery is decreased, based on an assessment of the decrease in flow rate.50. Consider a river that spreads out in a delta region on its way to the sea. Construct a problem in which you calculate the average speed at which water moves in the delta region, based on the speed at which it was moving up river. Among the things to consider are the size and flow rate of the river before it spreads out and its size once it has spread out. You can construct the problem for the river spreading out into one large river or into multiple smaller rivers.

# 12.5 The Onset of Turbulence

51. Verify that the flow of oil is laminar (barely) for an oil gusher that shoots crude oil  into the air through a pipe with a  diameter. The vertical pipe is  long. Take the density of the oil to be  and its viscosity to be  (or  .

52. Show that the Reynolds number  is unitless by substituting units for all the quantities in its definition and cancelling.

53. Calculate the Reynolds numbers for the flow of water through (a) a nozzle with a radius of 0.250 cm and (b) a garden hose with a radius of 0.900 cm, when the nozzle is attached to the hose. The flow rate through hose and nozzle is  . Can the flow in either possibly be laminar?

54. A fire hose has an inside diameter of  . Suppose such a hose carries a flow of  starting at a gauge pressure of . The hose goes  up a ladder to a nozzle having an inside diameter of  . Calculate the Reynolds numbers for flow in the fire hose and nozzle to show that the flow in each must be turbulent.

55. Concrete is pumped from a cement mixer to the place it is being laid, instead of being carried in wheelbarrows. The flow rate is  through a  -long, 8.00-cm-diameter hose, and the pressure at the pump is  . Verify that the flow of concrete is laminar taking concrete’s viscosity to be 48.0  , and given its density is  .

56. At what flow rate might turbulence begin to develop in a water main with a  diameter? Assume a  temperature.

57. What is the greatest average speed of blood flow at  in an artery of radius  if the flow is to remain laminar? What is the corresponding flow rate? Take the density of blood to be  .

58. In Take-Home Experiment: Inhalation, we measured the average flow rate  of air traveling through the trachea during each inhalation. Now calculate the average air speed in meters per second through your trachea during each inhalation. The radius of the trachea in adult humans is approximately  . From the data above, calculate the Reynolds number for the air flow in the trachea during inhalation. Do you expect the air flow to be laminar or turbulent?

59. Gasoline is piped underground from refineries to major users. The flow rate is  (about 500 gal/min), the viscosity of gasoline is   , and its density is  . (a) What minimum diameter must the pipe have if the Reynolds number is to be less than 2000? (b) What pressure difference must be maintained along each kilometer of the pipe to maintain this flow rate?

60. Assuming that blood is an ideal fluid, calculate the critical flow rate at which turbulence is a certainty in the aorta. Take the diameter of the aorta to be  . (Turbulence will actually occur at lower average flow rates, because blood is not an ideal fluid. Furthermore, since blood flow pulses, turbulence may occur during only the highvelocity part of each heartbeat.)

61. Unreasonable Results A fairly large garden hose has an internal radius of  and a length of  . The nozzleless horizontal hose is attached to a faucet, and it delivers  . (a) What water pressure is supplied by the faucet? (b) What is unreasonable about this pressure? (c) What is unreasonable about the premise? (d) What is the Reynolds number for the given flow? (Take the viscosity of water as 

# 12.7 Molecular Transport Phenomena: Diffusion, Osmosis, and Related Processes

62. You can smell perfume very shortly after opening the bottle. To show that it is not reaching your nose by diffusion, calculate the average distance a perfume molecule moves in one second in air, given its diffusion constant  to be  .

63. What is the ratio of the average distances that oxygen will diffuse in a given time in air and water? Why is this distance less in water (equivalently, why is  less in water)?64. Oxygen reaches the veinless cornea of the eye by diffusing through its tear layer, which is  thick. How long does it take the average oxygen molecule to do this?

65. (a) Find the average time required for an oxygen molecule to diffuse through a 0.200-mm-thick tear layer on the cornea. (b) How much time is required to diffuse  of oxygen to the cornea if its surface area is 

66. Suppose hydrogen and oxygen are diffusing through air. A small amount of each is released simultaneously. How much time passes before the hydrogen is 1.00 s ahead of the oxygen? Such differences in arrival times are used as an analytical tool in gas chromatography.