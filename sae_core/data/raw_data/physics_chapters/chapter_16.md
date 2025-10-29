# Chapter 16 - Oscillatory Motion and Waves
  
FIGURE 16.1 There are at least four types of waves in this picture—only the water waves are evident. There are also sound waves, light waves, and waves on the guitar strings. (credit: John Norton)

# CHAPTER OUTLINE

16.1 Hooke’s Law: Stress and Strain Revisited   
16.2 Period and Frequency in Oscillations   
16.3 Simple Harmonic Motion: A Special Periodic Motion   
16.4 The Simple Pendulum   
16.5 Energy and the Simple Harmonic Oscillator   
16.6 Uniform Circular Motion and Simple Harmonic Motion   
16.7 Damped Harmonic Motion   
16.8 Forced Oscillations and Resonance   
16.9 Waves   
16.10 Superposition and Interference   
16.11 Energy in Waves: Intensity

INTRODUCTION TO OSCILLATORY MOTION AND WAVES What do an ocean buoy, a child in a swing, the cone inside a speaker, a guitar, atoms in a crystal, the motion of chest cavities, and the beating of hearts all have in common? They all oscillate—-that is, they move back and forth between two points. Many systems oscillate, and they have certain characteristics in common. All oscillations involve force and energy. You push a child in a swing to get the motion started. The energy of atoms vibrating in a crystal can be increased with heat. You put energy into a guitar string when you pluck it.

Some oscillations create waves. A guitar creates sound waves. You can make water waves in a swimming pool by slapping the water with your hand. You can no doubt think of other types of waves. Some, such as water waves, arevisible. Some, such as sound waves, are not. But every wave is a disturbance that moves from its source and carries can behave like waves.

By studying oscillatory motion and waves, we shall find that a small number of underlying principles describe all of them and that wave phenomena are more common than you have ever imagined. We begin by studying the type of force that underlies the simplest oscillations and waves. We will then expand our exploration of oscillatory motion and waves to include concepts such as simple harmonic motion, uniform circular motion, and damped harmonic motion. Finally, we will explore what happens when two or more waves share the same space, in the phenomena known as superposition and interference.

Click to view content (https://openstax.org/books/college-physics-2e/pages/16-introduction-to-oscillatory-motionand-waves)

# 16.1 Hooke’s Law: Stress and Strain Revisited

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Explain Newton’s third law of motion with respect to stress and deformation. Describe the restoration of force and displacement. • Calculate the energy in Hooke’s Law of deformation, and the stored energy in a spring.

  
FIGURE 16.2 When displaced from its vertical equilibrium position, this plastic ruler oscillates back and forth because of the restoring force opposing displacement. When the ruler is on the left, there is a force to the right, and vice versa.

Newton’s first law implies that an object oscillating back and forth is experiencing forces. Without force, the object would move in a straight line at a constant speed rather than oscillate. Consider, for example, plucking a plastic ruler to the left as shown in Figure 16.2. The deformation of the ruler creates a force in the opposite direction, known as a restoring force. Once released, the restoring force causes the ruler to move back toward its stable equilibrium position, where the net force on it is zero. However, by the time the ruler gets there, it gains momentum and continues to move to the right, producing the opposite deformation. It is then forced to the left, back through equilibrium, and the process is repeated until dissipative forces dampen the motion. These forces remove mechanical energy from the system, gradually reducing the motion until the ruler comes to rest.

The simplest oscillations occur when the restoring force is directly proportional to displacement. When stress and strain were covered in Newton’s Third Law of Motion, the name was given to this relationship between force and displacement was Hooke’s law:



Here,  is the restoring force,  is the displacement from equilibrium or deformation, and  is a constant related to the difficulty in deforming the system. The minus sign indicates the restoring force is in the direction opposite to the displacement.  
FIGURE 16.3 (a) The plastic ruler has been released, and the restoring force is returning the ruler to its equilibrium position. (b) The net force is zero at the equilibrium position, but the ruler has momentum and continues to move to the right. (c) The restoring force is in the opposite direction. It stops the ruler and moves it back toward equilibrium again. (d) Now the ruler has momentum to the left. (e) In the absence of damping (caused by frictional forces), the ruler reaches its original position. From there, the motion will repeat itself.

The force constant  is related to the rigidity (or stiffness) of a system—the larger the force constant, the greater the restoring force, and the stiffer the system. The units of  are newtons per meter  . For example,  is directly related to Young’s modulus when we stretch a string. Figure 16.4 shows a graph of the absolute value of the restoring force versus the displacement for a system that can be described by Hooke’s law—a simple spring in this case. The slope of the graph equals the force constant  in newtons per meter. A common physics laboratory exercise is to measure restoring forces created by springs, determine if they follow Hooke’s law, and calculate their force constants if they do.

  
FIGURE 16.4 (a) A graph of absolute value of the restoring force versus displacement is displayed. The fact that the graph is a straight line means that the system obeys Hooke’s law. The slope of the graph is the force constant  . (b) The data in the graph were generated by measuring the displacement of a spring from equilibrium while supporting various weights. The restoring force equals the weight supported, if the mass is stationary.# EXAMPLE 16.1

# How Stiff Are Car Springs?

  
FIGURE 16.5 The mass of a car increases due to the introduction of a passenger. This affects the displacement of the car on its suspensio system. (credit: exfordy on Flickr)

What is the force constant for the suspension system of a car that settles  when an  person gets in?

# Strategy

Consider the car to be in its equilibrium position  before the person gets in. The car then settles down  , which means it is displaced to a position  At that point, the springs supply a restoring force  equal to the person’s weight  We take this force to be  in Hooke’s law. Knowing  and  , we can then solve the force constant  .

# Solution

1. Solve Hooke’s law,  , for  :



Substitute known values and solve  :



# Discussion

Note that  and  have opposite signs because they are in opposite directions—the restoring force is up, and the displacement is down. Also, note that the car would oscillate up and down when the person got in if it were not for damping (due to frictional forces) provided by shock absorbers. Bouncing cars are a sure sign of bad shock absorbers.

# Energy in Hooke’s Law of Deformation

In order to produce a deformation, work must be done. That is, a force must be exerted through a distance, whether you pluck a guitar string or compress a car spring. If the only result is deformation, and no work goes into thermal, sound, or kinetic energy, then all the work is initially stored in the deformed object as some form of potential energy. The potential energy stored in a spring is  . Here, we generalize the idea to elastic potential energy for a deformation of any system that can be described by Hooke’s law. Hence,

where  is the elastic potential energy stored in any deformed system that obeys Hooke’s law and has a displacement  from equilibrium and a force constant  .

It is possible to find the work done in deforming a system in order to find the energy stored. This work is performed by an applied force  . The applied force is exactly opposite to the restoring force (action-reaction), and so  . Figure 16.6 shows a graph of the applied force versus deformation  for a system that can be described by Hooke’s law. Work done on the system is force multiplied by distance, which equals the area under the curve or  (Method A in the figure). Another way to determine the work is to note that the force increases linearly from 0 to  , so that the average force is  , the distance moved is  , and thus   
 (Method B in the figure).

  
FIGURE 16.6 A graph of applied force versus distance for the deformation of a system that can be described by Hooke’s law is displayed. The work done on the system equals the area under the graph or the area of the triangle, which is half its base multiplied by its height, or  .

# EXAMPLE 16.2

# Calculating Stored Energy: A Toy Gun Spring

We can use a toy gun’s spring mechanism to ask and answer two simple questions: (a) How much energy is stored in the spring of a toy gun that has a force constant of  and is compressed  (b) If you neglect friction and the mass of the spring, at what speed will a  projectile be ejected from the gun?

  
FIGURE 16.7 (a) In this image of the gun, the spring is uncompressed before being cocked. (b) The spring has been compressed a distance , and the projectile is in place. (c) When released, the spring converts elastic potential energy  into kinetic energy.

# Strategy for a

(a): The energy stored in the spring can be found directly from elastic potential energy equation, because  and  are given.

# Solution for a

Entering the given values for  and  yields



# Strategy for b

Because there is no friction, the potential energy is converted entirely into kinetic energy. The expression for kinetic energy can be solved for the projectile’s speed.

# Solution for b

1. Identify known quantities:



2. Solve for  :



3. Convert units: 

# Discussion

(a) and (b): This projectile speed is impressive for a toy gun (more than  ). The numbers in this problem seem reasonable. The force needed to compress the spring is small enough for an adult to manage, and the energy imparted to the dart is small enough to limit the damage it might do, especially because the darts in many of these guns are made of soft material with a rubber tip. Yet, the speed of the dart is great enough for it to travel an acceptable distance.

# CHECK YOUR UNDERSTANDING

Envision holding the end of a ruler with one hand and deforming it with the other. When you let go, you can see the oscillations of the ruler. In what way could you modify this simple experiment to increase the rigidity of the system?

# Solution

You could hold the ruler at its midpoint so that the part of the ruler that oscillates is half as long as in the original experiment.

# CHECK YOUR UNDERSTANDING

If you apply a deforming force on an object and let it come to equilibrium, what happened to the work you did on the system?

# Solution

It was stored in the object as potential energy.

# 16.2 Period and Frequency in Oscillations

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

• Observe the vibrations of a guitar string. Determine the frequency of oscillations.  
FIGURE 16.8 The strings on this guitar vibrate at regular time intervals. (credit: JAR)

When you pluck a guitar string, the resulting sound has a steady tone and lasts a long time. Each successive vibration of the string takes the same time as the previous one. We define periodic motion to be a motion that repeats itself at regular time intervals, such as exhibited by the guitar string or by an object on a spring moving up and down. The time to complete one oscillation remains constant and is called the period  . Its units are usually seconds, but may be any convenient unit of time. The word period refers to the time for some event whether repetitive or not; but we shall be primarily interested in periodic motion, which is by definition repetitive. A concept closely related to period is the frequency of an event. For example, if you get a paycheck twice a month, the frequency of payment is two per month and the period between checks is half a month. Frequency  is defined to be the number of events per unit time. For periodic motion, frequency is the number of oscillations per unit time. The relationship between frequency and period is



The SI unit for frequency is the cycle per second, which is defined to be a hertz  :



A cycle is one complete oscillation. Note that a vibration can be a single or multiple event, whereas oscillations are usually repetitive for a significant number of cycles.

# EXAMPLE 16.3

# Determine the Frequency of Two Oscillations: Medical Ultrasound and the Period of Middle C

We can use the formulas presented in this module to determine both the frequency based on known oscillations and the oscillation based on a known frequency. Let’s try one example of each. (a) A medical imaging device produces ultrasound by oscillating with a period of  . What is the frequency of this oscillation? (b) The frequency of middle C on a typical musical instrument is  . What is the time for one complete oscillation?

# Strategy

Both questions (a) and (b) can be answered using the relationship between period and frequency. In question (a), the period  is given and we are asked to find frequency  . In question (b), the frequency  is given and we are asked to find the period  .

# Solution a

1. Substitute  for  in 



Solve to find

# Discussion a

The frequency of sound found in (a) is much higher than the highest frequency that humans can hear and, therefore, is called ultrasound. Appropriate oscillations at this frequency generate ultrasound used for noninvasive medical diagnoses, such as observations of a fetus in the womb.

# Solution b

1. Identify the known values: The time for one complete oscillation is the period  :



2. Solve for  :



3. Substitute the given value for the frequency into the resulting expression:



# Discussion b

The period found in (b) is the time per cycle, but this value is often quoted as simply the time in convenient units (ms or milliseconds in this case).

# CHECK YOUR UNDERSTANDING

Identify an event in your life (such as receiving a paycheck) that occurs regularly. Identify both the period and frequency of this event.

# Solution

I visit my parents for dinner every other Sunday. The frequency of my visits is 26 per calendar year. The period is two weeks.

# 16.3 Simple Harmonic Motion: A Special Periodic Motion

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Describe a simple harmonic oscillator.   
Explain the link between simple harmonic motion and waves.

The oscillations of a system in which the net force can be described by Hooke’s law are of special importance, because they are very common. They are also the simplest oscillatory systems. Simple Harmonic Motion (SHM) is the name given to oscillatory motion for a system where the net force can be described by Hooke’s law, and such a system is called a simple harmonic oscillator. If the net force can be described by Hooke’s law and there is no displacement on either side of the equilibrium position, as shown for an object on a spring in Figure 16.9. The maximum displacement from equilibrium is called the amplitude  . The units for amplitude and displacement are the same, but depend on the type of oscillation. For the object on the spring, the units of amplitude and displacement are meters; whereas for sound oscillations, they have units of pressure (and other types of oscillations have yet other units). Because amplitude is the maximum displacement, it is related to the energy in the oscillation.

# Take-Home Experiment: SHM and the Marble

Find a bowl or basin that is shaped like a hemisphere on the inside. Place a marble inside the bowl and tilt the bowl periodically so the marble rolls from the bottom of the bowl to equally high points on the sides of the bowl.Get a feel for the force required to maintain this periodic motion. What is the restoring force and what role does the force you apply play in the simple harmonic motion (SHM) of the marble?

  
FIGURE 16.9 An object attached to a spring sliding on a frictionless surface is an uncomplicated simple harmonic oscillator. When displaced from equilibrium, the object performs simple harmonic motion that has an amplitude  and a period  . The object’s maximum speed occurs as it passes through equilibrium. The stiffer the spring is, the smaller the period  . The greater the mass of the object is, the greater the period  .

What is so significant about simple harmonic motion? One special thing is that the period  and frequency  of a simple harmonic oscillator are independent of amplitude. The string of a guitar, for example, will oscillate with the same frequency whether plucked gently or hard. Because the period is constant, a simple harmonic oscillator can be used as a clock.

Two important factors do affect the period of a simple harmonic oscillator. The period is related to how stiff the system is. A very stiff object has a large force constant  , which causes the system to have a smaller period. For example, you can adjust a diving board’s stiffness—the stiffer it is, the faster it vibrates, and the shorter its period. Period also depends on the mass of the oscillating system. The more massive the system is, the longer the period. For example, a heavy person on a diving board bounces up and down more slowly than a light one.

In fact, the mass and the force constant  are the only factors that affect the period and frequency of simple harmonic motion.

# Period of Simple Harmonic Oscillator

The period of a simple harmonic oscillator is given by



and, because  , the frequency of a simple harmonic oscillator is



Note that neither  nor  has any dependence on amplitude.# Take-Home Experiment: Mass and Ruler Oscillations

Find two identical wooden or plastic rulers. Tape one end of each ruler firmly to the edge of a table so that the length of each ruler that protrudes from the table is the same. On the free end of one ruler tape a heavy object such as a few large coins. Pluck the ends of the rulers at the same time and observe which one undergoes more cycles in a time period, and measure the period of oscillation of each of the rulers.

# EXAMPLE 16.4

# Calculate the Frequency and Period of Oscillations: Bad Shock Absorbers in a Car

If the shock absorbers in a car go bad, then the car will oscillate at the least provocation, such as when going over bumps in the road and after stopping (See Figure 16.10). Calculate the frequency and period of these oscillations for such a car if the car’s mass (including its load) is  and the force constant  of the suspension system is  .

# Strategy

The frequency of the car’s oscillations will be that of a simple harmonic oscillator as given in the equation  . The mass and the force constant are both given.

# Solution

1. Enter the known values of  and  :



2. Calculate the frequency:



3. You could use  to calculate the period, but it is simpler to use the relationship  and substitute the value just found for  :



# Discussion

The values of  and  both seem about right for a bouncing car. You can observe these oscillations if you push down hard on the end of a car and let go.

# The Link between Simple Harmonic Motion and Waves

If a time-exposure photograph of the bouncing car were taken as it drove by, the headlight would make a wavelike streak, as shown in Figure 16.10. Similarly, Figure 16.11 shows an object bouncing on a spring as it leaves a wavelike "trace" of its position on a moving strip of paper. Both waves are sine functions. All simple harmonic motion is intimately related to sine and cosine waves.

  
FIGURE 16.10 The bouncing car makes a wavelike motion. If the restoring force in the suspension system can be described only by Hooke’s law, then the wave is a sine function. (The wave is the trace produced by the headlight as the car moves to the right.)  
FIGURE 16.11 The vertical position of an object bouncing on a spring is recorded on a strip of moving paper, leaving a sine wave.

The displacement as a function of time t in any simple harmonic motion—that is, one in which the net restoring forc can be described by Hooke’s law, is given by



where  is amplitude. At  , the initial position is  , and the displacement oscillates back and forth with a period  . (When  , we get  again because  ). Furthermore, from this expression for  , the velocity  as a function of time is given by:



where  . The object has zero velocity at maximum displacement—for example,  when  , and at that time  . The minus sign in the first equation for  gives the correct direction for the velocity. Just after the start of the motion, for instance, the velocity is negative because the system is moving back toward the equilibrium point. Finally, we can get an expression for acceleration using Newton’s second law. [Then we have  and  , the quantities needed for kinematics and a description of simple harmonic motion.] According to Newton’s second law, the acceleration is  . So,  is also a cosine function:



Hence,  is directly proportional to and in the opposite direction to  .

Figure 16.12 shows the simple harmonic motion of an object on a spring and presents graphs of  and  versus time.  
FIGURE 16.12 Graphs of  and  versus  for the motion of an object on a spring. The net force on the object can be described by Hooke’s law, and so the object undergoes simple harmonic motion. Note that the initial position has the vertical displacement at its maximum value  ;  is initially zero and then negative as the object moves down; and the initial acceleration is negative, back toward the equilibrium position and becomes zero at that point.

The most important point here is that these equations are mathematically straightforward and are valid for all simple harmonic motion. They are very useful in visualizing waves associated with simple harmonic motion, including visualizing how waves add with one another.

# CHECK YOUR UNDERSTANDING

Suppose you pluck a banjo string. You hear a single note that starts out loud and slowly quiets over time. Describe what happens to the sound waves in terms of period, frequency and amplitude as the sound decreases in volume.

# Solution

Frequency and period remain essentially unchanged. Only amplitude decreases as volume decreases.

# CHECK YOUR UNDERSTANDING

A babysitter is pushing a child on a swing. At the point where the swing reaches  , where would the corresponding point on a wave of this motion be located?# Solution

 is the maximum deformation, which corresponds to the amplitude of the wave. The point on the wave would either be at the very top or the very bottom of the curve.

# PHET EXPLORATIONS

# Masses and Springs

A realistic mass and spring laboratory. Hang masses from springs and adjust the spring stiffness and damping. You can even slow time. Transport the lab to different planets. A chart shows the kinetic, potential, and thermal energy for each spring.

Click to view content (https://openstax.org/books/college-physics-2e/pages/16-3-simple-harmonic-motion-aspecial-periodic-motion)

# 16.4 The Simple Pendulum

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

• Measure acceleration due to gravity.

  
FIGURE 16.13 A simple pendulum has a small-diameter bob and a string that has a very small mass but is strong enough not to stretch appreciably. The linear displacement from equilibrium is  , the length of the arc. Also shown are the forces on the bob, which result in a net force of toward the equilibrium position—that is, a restoring force.

Pendulums are in common usage. Some have crucial uses, such as in clocks; some are for fun, such as a child’s swing; and some are just there, such as the sinker on a fishing line. For small displacements, a pendulum is a simple harmonic oscillator. A simple pendulum is defined to have an object that has a small mass, also known as the pendulum bob, which is suspended from a light wire or string, such as shown in Figure 16.13. Exploring the simple pendulum a bit further, we can discover the conditions under which it performs simple harmonic motion, and we can derive an interesting expression for its period.

We begin by defining the displacement to be the arc length . We see from Figure 16.13 that the net force on the bob is tangent to the arc and equals  sin  . (The weight has components  cos  along the string and mg sin  tangent to the arc.) Tension in the string exactly cancels the component  parallel to the string. This leaves a net restoring force back toward the equilibrium position at  .

Now, if we can show that the restoring force is directly proportional to the displacement, then we have a simple harmonic oscillator. In trying to determine if we have a simple harmonic oscillator, we should note that for small angles (less than about  ,  (  and  differ by about  or less at smaller angles). Thus, for angles less than about  , the restoring force  is



The displacement  is directly proportional to  . When  is expressed in radians, the arc length in a circle is related to its radius (  in this instance) by:

so that



For small angles, then, the expression for the restoring force is:



This expression is of the form:



where the force constant is given by  and the displacement is given by  . For angles less than about  , the restoring force is directly proportional to the displacement, and the simple pendulum is a simple harmonic oscillator.

Using this equation, we can find the period of a pendulum for amplitudes less than about  . For the simple pendulum:



Thus,



for the period of a simple pendulum. This result is interesting because of its simplicity. The only things that affect the period of a simple pendulum are its length and the acceleration due to gravity. The period is completely independent of other factors, such as mass. As with simple harmonic oscillators, the period  for a pendulum is nearly independent of amplitude, especially if  is less than about  . Even simple pendulum clocks can be finely adjusted and accurate.

Note the dependence of  on  . If the length of a pendulum is precisely known, it can actually be used to measure the acceleration due to gravity. Consider the following example.

# EXAMPLE 16.5

# Measuring Acceleration due to Gravity: The Period of a Pendulum

What is the acceleration due to gravity in a region where a simple pendulum having a length  has a period of 1.7357 s?

# Strategy

We are asked to find  given the period  and the length  of a pendulum. We can solve  for , assuming only that the angle of deflection is less than  .

# Solution

1. Square  and solve for  :



2. Substitute known values into the new equation:



# Discussion

This method for determining can be very accurate. This is why length and period are given to five digits in this example. For the precision of the approximation  to be better than the precision of the pendulum length and period, the maximum displacement angle should be kept below about  .

# Making Career Connections

Knowing can be important in geological exploration; for example, a map of  over large geographical regions aids the study of plate tectonics and helps in the search for oil fields and large mineral deposits.

# Take Home Experiment: Determining

Use a simple pendulum to determine the acceleration due to gravity  in your own locale. Cut a piece of a string or dental floss so that it is about  long. Attach a small object of high density to the end of the string (for example, a metal nut or a car key). Starting at an angle of less than  , allow the pendulum to swing and measure the pendulum’s period for 10 oscillations using a stopwatch. Calculate  . How accurate is this measurement? How might it be improved?

# CHECK YOUR UNDERSTANDING

An engineer builds two simple pendula. Both are suspended from small wires secured to the ceiling of a room. Each pendulum hovers 2 cm above the floor. Pendulum 1 has a bob with a mass of  . Pendulum 2 has a bob with a mass of  . Describe how the motion of the pendula will differ if the bobs are both displaced by  .

# Solution

The movement of the pendula will not differ at all because the mass of the bob has no effect on the motion of a simple pendulum. The pendula are only affected by the period (which is related to the pendulum’s length) and by the acceleration due to gravity.

# PHET EXPLORATIONS

# Pendulum Lab

Play with one or two pendulums and discover how the period of a simple pendulum depends on the length of the string, the mass of the pendulum bob, and the amplitude of the swing. It’s easy to measure the period using the photogate timer. You can vary friction and the strength of gravity. Use the pendulum to find the value of  on planet X. Notice the anharmonic behavior at large amplitude.

Click to view content (https://openstax.org/books/college-physics-2e/pages/16-4-the-simple-pendulum)

# 16.5 Energy and the Simple Harmonic Oscillator

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

• Determine the maximum speed of an oscillating system.

To study the energy of a simple harmonic oscillator, we first consider all the forms of energy it can have We know from Hooke’s Law: Stress and Strain Revisited that the energy stored in the deformation of a simple harmonic oscillator is a form of potential energy given by:

Because a simple harmonic oscillator has no dissipative forces, the other important form of energy is kinetic energy . Conservation of energy for these two forms is:



or



This statement of conservation of energy is valid for all simple harmonic oscillators, including ones where the gravitational force plays a role

Namely, for a simple pendulum we replace the velocity with  , the spring constant with  , and the displacement term with  . Thus



In the case of undamped simple harmonic motion, the energy oscillates back and forth between kinetic and potential, going completely from one to the other as the system oscillates. So for the simple example of an object on a frictionless surface attached to a spring, as shown again in Figure 16.14, the motion starts with all of the energy stored in the spring. As the object starts to move, the elastic potential energy is converted to kinetic energy, becoming entirely kinetic energy at the equilibrium position. It is then converted back into elastic potential energy by the spring, the velocity becomes zero when the kinetic energy is completely converted, and so on. This concept provides extra insight here and in later applications of simple harmonic motion, such as alternating current circuits.

  
FIGURE 16.14 The transformation of energy in simple harmonic motion is illustrated for an object attached to a spring on a frictionless surface.

The conservation of energy principle can be used to derive an expression for velocity  . If we start our simple harmonic motion with zero velocity and maximum displacement  , then the total energy is



This total energy is constant and is shifted back and forth between kinetic energy and potential energy, at mosttimes being shared by each. The conservation of energy for this system in equation form is thus:



Solving this equation for  yields:



Manipulating this expression algebraically gives:



and so



where



From this expression, we see that the velocity is a maximum  at  , as stated earlier in  sin  proportional to amplitude. As you might guess, the greater the maximum displacement the greater the maximum velocity. Maximum velocity is also greater for stiffer systems, because they exert greater force for the same displacement. This observation is seen in the expression for  it is proportional to the square root of the force constant  . Finally, the maximum velocity is smaller for objects that have larger masses, because the maximum velocity is inversely proportional to the square root of  . For a given force, objects that have large masses accelerate more slowly.

A similar calculation for the simple pendulum produces a similar result, namely:



# EXAMPLE 16.6

# Determine the Maximum Speed of an Oscillating System: A Bumpy Road

Suppose that a car is  and has a suspension system that has a force constant  . The car hits a bump and bounces with an amplitude of  . What is its maximum vertical velocity if you assume no damping occurs?

# Strategy

We can use the expression for  given in  to determine the maximum vertical velocity. The variables  and  are given in the problem statement, and the maximum displacement  is  .

# Solution

1. Identify known.   
2. Substitute known values into 

3. Calculate to find 

# Discussion

This answer seems reasonable for a bouncing car. There are other ways to use conservation of energy to find  We could use it directly, as was done in the example featured in Hooke’s Law: Stress and Strain Revisited.

The small vertical displacement  of an oscillating simple pendulum, starting from its equilibrium position, is given as



where  is the amplitude,  is the angular velocity and  is the time taken. Substituting  , we have



Thus, the displacement of pendulum is a function of time as shown above.

Also the velocity of the pendulum is given by



so the motion of the pendulum is a function of time.

# CHECK YOUR UNDERSTANDING

Why does it hurt more if your hand is snapped with a ruler than with a loose spring, even if the displacement of each system is equal?

# Solution

The ruler is a stiffer system, which carries greater force for the same amount of displacement. The ruler snaps your hand with greater force, which hurts more.

# CHECK YOUR UNDERSTANDING

You are observing a simple harmonic oscillator. Identify one way you could decrease the maximum velocity of the system.

# Solution

You could increase the mass of the object that is oscillating.

# 16.6 Uniform Circular Motion and Simple Harmonic Motion

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

• Compare simple harmonic motion with uniform circular motion.  
FIGURE 16.15 The horses on this merry-go-round exhibit uniform circular motion. (credit: Wonderlane, Flickr)

There is an easy way to produce simple harmonic motion by using uniform circular motion. Figure 16.16 shows one way of using this method. A ball is attached to a uniformly rotating vertical turntable, and its shadow is projected on the floor as shown. The shadow undergoes simple harmonic motion. Hooke’s law usually describes uniform circular motions (  constant) rather than systems that have large visible displacements. So observing the projection of uniform circular motion, as in Figure 16.16, is often easier than observing a precise large-scale simple harmonic oscillator. If studied in sufficient depth, simple harmonic motion produced in this manner can give considerable insight into many aspects of oscillations and waves and is very useful mathematically. In our brief treatment, we shall indicate some of the major features of this relationship and how they might be useful.

Shadow undergoes simple harmonic oscillation

  
FIGURE 16.16 The shadow of a ball rotating at constant angular velocity  on a turntable goes back and forth in precise simple harmonic motion.

Figure 16.17 shows the basic relationship between uniform circular motion and simple harmonic motion. The point P travels around the circle at constant angular velocity  . The point P is analogous to an object on the merry-goround. The projection of the position of P onto a fixed axis undergoes simple harmonic motion and is analogous to the shadow of the object. At the time shown in the figure, the projection has position  and moves to the left with velocity  . The velocity of the point P around the circle equals  .The projection of  on the  -axis is the velocity  of the simple harmonic motion along the  -axis.  
FIGURE 16.17 A point P moving on a circular path with a constant angular velocity  is undergoing uniform circular motion. Its projection on the  -axis undergoes simple harmonic motion. Also shown is the velocity of this point around the circle,  , and its projection, which is  . Note that these velocities form a similar triangle to the displacement triangle.

To see that the projection undergoes simple harmonic motion, note that its position  is given by



where  ,  is the constant angular velocity, and  is the radius of the circular path. Thus,



The angular velocity  is in radians per unit time; in this case  radians is the time for one revolution  . That is,  . Substituting this expression for  , we see that the position  is given by:



This expression is the same one we had for the position of a simple harmonic oscillator in Simple Harmonic Motion: A Special Periodic Motion. If we make a graph of position versus time as in Figure 16.18, we see again the wavelike character (typical of simple harmonic motion) of the projection of uniform circular motion onto the  -axis.

  
FIGURE 16.18 The position of the projection of uniform circular motion performs simple harmonic motion, as this wavelike graph of  versus indicates.

Now let us use Figure 16.17 to do some further analysis of uniform circular motion as it relates to simple harmonic motion. The triangle formed by the velocities in the figure and the triangle formed by the displacements  and  are similar right triangles. Taking ratios of similar sides, we see that

We can solve this equation for the speed  or



This expression for the speed of a simple harmonic oscillator is exactly the same as the equation obtained from conservation of energy considerations in Energy and the Simple Harmonic Oscillator.You can begin to see that it is possible to get all of the characteristics of simple harmonic motion from an analysis of the projection of uniform circular motion.

Finally, let us consider the period  of the motion of the projection. This period is the time it takes the point P to complete one revolution. That time is the circumference of the circle  divided by the velocity around the circle,  . Thus, the period  is



We know from conservation of energy considerations that



Solving this equation for  gives



Substituting this expression into the equation for  yields



Thus, the period of the motion is the same as for a simple harmonic oscillator. We have determined the period for any simple harmonic oscillator using the relationship between uniform circular motion and simple harmonic motion.

Some modules occasionally refer to the connection between uniform circular motion and simple harmonic motion. Moreover, if you carry your study of physics and its applications to greater depths, you will find this relationship useful. It can, for example, help to analyze how waves add when they are superimposed.

# CHECK YOUR UNDERSTANDING

Identify an object that undergoes uniform circular motion. Describe how you could trace the simple harmonic motion of this object as a wave.

# Solution

A record player undergoes uniform circular motion. You could attach dowel rod to one point on the outside edge of the turntable and attach a pen to the other end of the dowel. As the record player turns, the pen will move. You can drag a long piece of paper under the pen, capturing its motion as a wave.

# 16.7 Damped Harmonic Motion

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Compare and discuss underdamped and overdamped oscillating systems.   
Explain critically damped system.  
FIGURE 16.19 In order to counteract dampening forces, this mom needs to keep pushing the swing. (credit: Erik A. Johnson, Flickr)

A guitar string stops oscillating a few seconds after being plucked. To keep a child happy on a swing, you must keep pushing. Although we can often make friction and other non-conservative forces negligibly small, completely undamped motion is rare. In fact, we may even want to damp oscillations, such as with car shock absorbers.

For a system that has a small amount of damping, the period and frequency are nearly the same as for simple harmonic motion, but the amplitude gradually decreases as shown in Figure 16.20. This occurs because the nonconservative damping force removes energy from the system, usually in the form of thermal energy. In general, energy removal by non-conservative forces is described as



where  is work done by a non-conservative force (here the damping force). For a damped harmonic oscillator,  is negative because it removes mechanical energy  ) from the system.

  
FIGURE 16.20 In this graph of displacement versus time for a harmonic oscillator with a small amount of damping, the amplitude slowly decreases, but the period and frequency are nearly the same as if the system were completely undamped.

If you gradually increase the amount of damping in a system, the period and frequency begin to be affected, because damping opposes and hence slows the back and forth motion. (The net force is smaller in both directions.) If there is very large damping, the system does not even oscillate—it slowly moves toward equilibrium. Figure 16.21 shows the displacement of a harmonic oscillator for different amounts of damping. When we want to damp out oscillations, such as in the suspension of a car, we may want the system to return to equilibrium as quickly as possible Critical damping is defined as the condition in which the damping of an oscillator results in it returning as quickly as possible to its equilibrium position The critically damped system may overshoot the equilibrium position, but if it does, it will do so only once. Critical damping is represented by Curve A in Figure 16.21. With less-than critical damping, the system will return to equilibrium faster but will overshoot and cross over one or more times. Such a system is underdamped; its displacement is represented by the curve in Figure 16.20. Curve B in Figure 16.21 represents an overdamped system. As with critical damping, it too may overshoot the equilibrium position, but will reach equilibrium over a longer period of time.  
FIGURE 16.21 Displacement versus time for a critically damped harmonic oscillator (A) and an overdamped harmonic oscillator (B). The critically damped oscillator returns to equilibrium at  in the smallest time possible without overshooting.

Critical damping is often desired, because such a system returns to equilibrium rapidly and remains at equilibrium as well. In addition, a constant force applied to a critically damped system moves the system to a new equilibrium position in the shortest time possible without overshooting or oscillating about the new position. For example, when you stand on bathroom scales that have a needle gauge, the needle moves to its equilibrium position without oscillating. It would be quite inconvenient if the needle oscillated about the new equilibrium position for a long time before settling. Damping forces can vary greatly in character. Friction, for example, is sometimes independent of velocity (as assumed in most places in this text). But many damping forces depend on velocity—sometimes in complex ways, sometimes simply being proportional to velocity.

# EXAMPLE 16.7

# Damping an Oscillatory Motion: Friction on an Object Connected to a Spring

Damping oscillatory motion is important in many systems, and the ability to control the damping is even more so. This is generally attained using non-conservative forces such as the friction between surfaces, and viscosity for objects moving through fluids. The following example considers friction. Suppose a  object is connected to a spring as shown in Figure 16.22, but there is simple friction between the object and the surface, and the coefficient of friction  is equal to 0.0800. (a) What is the frictional force between the surfaces? (b) What total distance does the object travel if it is released  from equilibrium, starting at  The force constant of the spring is  .

  
FIGURE 16.22 The transformation of energy in simple harmonic motion is illustrated for an object attached to a spring on a frictionless surface.# Strategy

This problem requires you to integrate your knowledge of various concepts regarding waves, oscillations, and damping. To solve an integrated concept problem, you must first identify the physical principles involved. Part (a) is about the frictional force. This is a topic involving the application of Newton’s Laws. Part (b) requires an understanding of work and conservation of energy, as well as some understanding of horizontal oscillatory systems.

Now that we have identified the principles we must apply in order to solve the problems, we need to identify the knowns and unknowns for each part of the question, as well as the quantity that is constant in Part (a) and Part (b) of the question.

# Solution a

1. Choose the proper equation: Friction is  .   
2. Identify the known values.   
3. Enter the known values into the equation: 

4. Calculate and convert units: 

# Discussion a

The force here is small because the system and the coefficients are small.

# Solution b

Identify the known:

• The system involves elastic potential energy as the spring compresses and expands, friction that is related to the work done, and the kinetic energy as the body speeds up and slows down. Energy is not conserved as the mass oscillates because friction is a non-conservative force. The motion is horizontal, so gravitational potential energy does not need to be considered. Because the motion starts from rest, the energy in the system is initially  . This energy is removed by work done by friction  , where  is the total distance traveled and  is the force of friction. When the system stops moving, the friction force will balance the force exerted by the spring, so  where  is the final position and is given by



1. By equating the work done to the energy removed, solve for the distance  .

2. The work done by the non-conservative forces equals the initial, stored elastic potential energy. Identify the correct equation to use:



3. Recall that  .

4. Enter the friction as  into  , thus



5. Combine these two equations to find



6. Solve the equation for  :



7. Enter the known values into the resulting equation:

8. Calculate  and convert units:



# Discussion b

This is the total distance traveled back and forth across  , which is the undamped equilibrium position. The number of oscillations about the equilibrium position will be more than  because the amplitude of the oscillations is decreasing with time. At the end of the motion, this system will not return to  for this type of damping force, because static friction will exceed the restoring force. This system is underdamped. In contrast, an overdamped system with a simple constant damping force would not cross the equilibrium position  a single time. For example, if this system had a damping force 20 times greater, it would only move  toward the equilibrium position from its original  position.

This worked example illustrates how to apply problem-solving strategies to situations that integrate the different concepts you have learned. The first step is to identify the physical principles involved in the problem. The second step is to solve for the unknowns using familiar problem-solving strategies. These are found throughout the text, and many worked examples show how to use them for single topics. In this integrated concepts example, you can see how to apply them across several topics. You will find these techniques useful in applications of physics outside a physics course, such as in your profession, in other science disciplines, and in everyday life.

# CHECK YOUR UNDERSTANDING

Why are completely undamped harmonic oscillators so rare?

# Solution

Friction often comes into play whenever an object is moving. Friction causes damping in a harmonic oscillator.

# CHECK YOUR UNDERSTANDING

Describe the difference between overdamping, underdamping, and critical damping.

# Solution

An overdamped system moves slowly toward equilibrium. An underdamped system moves quickly to equilibrium, but will oscillate about the equilibrium point as it does so. A critically damped system moves as quickly as possible toward equilibrium without oscillating about the equilibrium.

# 16.8 Forced Oscillations and Resonance

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

• Observe resonance of a paddle ball on a string.   
• Observe amplitude of a damped harmonic oscillator.  
FIGURE 16.23 You can cause the strings in a piano to vibrate simply by producing sound waves from your voice. (credit: Matt Billings, Flickr)

Sit in front of a piano sometime and sing a loud brief note at it with the dampers off its strings. It will sing the same note back at you—the strings, having the same frequencies as your voice, are resonating in response to the forces from the sound waves that you sent to them. Your voice and a piano’s strings is a good example of the fact that objects—in this case, piano strings—can be forced to oscillate but oscillate best at their natural frequency. In this section, we shall briefly explore applying a periodic driving force acting on a simple harmonic oscillator. The driving force puts energy into the system at a certain frequency, not necessarily the same as the natural frequency of the system. The natural frequency is the frequency at which a system would oscillate if there were no driving and no damping force.

Most of us have played with toys involving an object supported on an elastic band, something like the paddle ball suspended from a finger in Figure 16.24. Imagine the finger in the figure is your finger. At first you hold your finger steady, and the ball bounces up and down with a small amount of damping. If you move your finger up and down slowly, the ball will follow along without bouncing much on its own. As you increase the frequency at which you move your finger up and down, the ball will respond by oscillating with increasing amplitude. When you drive the ball at its natural frequency, the ball’s oscillations increase in amplitude with each oscillation for as long as you drive it. The phenomenon of driving a system with a frequency equal to its natural frequency is called resonance. A system being driven at its natural frequency is said to resonate. As the driving frequency gets progressively higher than the resonant or natural frequency, the amplitude of the oscillations becomes smaller, until the oscillations nearly disappear and your finger simply moves up and down with little effect on the ball.

  
FIGURE 16.24 The paddle ball on its rubber band moves in response to the finger supporting it. If the finger moves with the natural frequency  of the ball on the rubber band, then a resonance is achieved, and the amplitude of the ball’s oscillations increases dramatically. At higher and lower driving frequencies, energy is transferred to the ball less efficiently, and it responds with lower-amplitude oscillations.

Figure 16.25 shows a graph of the amplitude of a damped harmonic oscillator as a function of the frequency of the periodic force driving it. There are three curves on the graph, each representing a different amount of damping. All three curves peak at the point where the frequency of the driving force equals the natural frequency of the harmonic oscillator. The highest peak, or greatest response, is for the least amount of damping, because less energy isremoved by the damping force.

  
FIGURE 16.25 Amplitude of a harmonic oscillator as a function of the frequency of the driving force. The curves represent the same oscillator with the same natural frequency but with different amounts of damping. Resonance occurs when the driving frequency equals the natural frequency, and the greatest response is for the least amount of damping. The narrowest response is also for the least damping.

It is interesting that the widths of the resonance curves shown in Figure 16.25 depend on damping: the less the damping, the narrower the resonance. The message is that if you want a driven oscillator to resonate at a very specific frequency, you need as little damping as possible. Little damping is the case for piano strings and many other musical instruments. Conversely, if you want small-amplitude oscillations, such as in a car’s suspension system, then you want heavy damping. Heavy damping reduces the amplitude, but the tradeoff is that the system responds at more frequencies.

These features of driven harmonic oscillators apply to a huge variety of systems. When you tune a radio, for example, you are adjusting its resonant frequency so that it only oscillates to the desired station’s broadcast (driving) frequency. The more selective the radio is in discriminating between stations, the smaller its damping. Magnetic resonance imaging (MRI) is a widely used medical diagnostic tool in which atomic nuclei (mostly hydrogen nuclei) are made to resonate by incoming radio waves (on the order of  ). A child on a swing is driven by a parent at the swing’s natural frequency to achieve maximum amplitude. In all of these cases, the efficiency of energy transfer from the driving force into the oscillator is best at resonance. Speed bumps and gravel roads prove that even a car’s suspension system is not immune to resonance. In spite of finely engineered shock absorbers, which ordinarily convert mechanical energy to thermal energy almost as fast as it comes in, speed bumps still cause a large-amplitude oscillation. On gravel roads that are corrugated, you may have noticed that if you travel at the “wrong” speed, the bumps are very noticeable whereas at other speeds you may hardly feel the bumps at all. Figure 16.26 shows a photograph of a famous example (the Tacoma Narrows Bridge) of the destructive effects of a driven harmonic oscillation. The Millennium Bridge in London was closed for a short period of time for the same reason while inspections were carried out.

In our bodies, the chest cavity is a clear example of a system at resonance. The diaphragm and chest wall drive the oscillations of the chest cavity which result in the lungs inflating and deflating. The system is critically damped and the muscular diaphragm oscillates at the resonant value for the system, making it highly efficient.  
FIGURE 16.26 In 1940, the Tacoma Narrows Bridge in Washington state collapsed. Heavy cross winds drove the bridge into oscillations at its resonant frequency. Damping decreased when support cables broke loose and started to slip over the towers, allowing increasingly greater amplitudes until the structure failed (credit: PRI's Studio 360, via Flickr)

# CHECK YOUR UNDERSTANDING

A famous magic trick involves a performer singing a note toward a crystal glass until the glass shatters. Explain why the trick works in terms of resonance and natural frequency.

# Solution

The performer must be singing a note that corresponds to the natural frequency of the glass. As the sound wave is directed at the glass, the glass responds by resonating at the same frequency as the sound wave. With enough energy introduced into the system, the glass begins to vibrate and eventually shatters.

# 16.9 Waves

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

• State the characteristics of a wave.   
• Calculate the velocity of wave propagation.

  
FIGURE 16.27 Waves in the ocean behave similarly to all other types of waves. (credit: Steve Jurveston, Flickr)

What do we mean when we say something is a wave? The most intuitive and easiest wave to imagine is the familiar water wave. More precisely, a wave is a disturbance that propagates, or moves from the place it was created. For water waves, the disturbance is in the surface of the water, perhaps created by a rock thrown into a pond or by a swimmer splashing the surface repeatedly. For sound waves, the disturbance is a change in air pressure, perhaps created by the oscillating cone inside a speaker. For earthquakes, there are several types of disturbances, including disturbance of Earth’s surface and pressure disturbances under the surface. Even radio waves are most easily understood using an analogy with water waves. Visualizing water waves is useful because there is more to it than just a mental image. Water waves exhibit characteristics common to all waves, such as amplitude, period, frequency and energy. All wave characteristics can be described by a small set of underlying principles.

A wave is a disturbance that propagates, or moves from the place it was created. The simplest waves repeatthemselves for several cycles and are associated with simple harmonic motion. Let us start by considering the simplified water wave in Figure 16.28. The wave is an up and down disturbance of the water surface. It causes a sea gull to move up and down in simple harmonic motion as the wave crests and troughs (peaks and valleys) pass under the bird. The time for one complete up and down motion is the wave’s period  . The wave’s frequency is  , as usual. The wave itself moves to the right in the figure. This movement of the wave is actually the disturbance moving to the right, not the water itself (or the bird would move to the right). We define wave velocity  to be the speed at which the disturbance moves. Wave velocity is sometimes also called the propagation velocity or propagation speed, because the disturbance propagates from one location to another.

# Misconception Alert

Many people think that water waves push water from one direction to another. In fact, the particles of water tend to stay in one location, save for moving up and down due to the energy in the wave. The energy moves forward through the water, but the water stays in one place. If you feel yourself pushed in an ocean, what you feel is the energy of the wave, not a rush of water.

  
FIGURE 16.28 An idealized ocean wave passes under a sea gull that bobs up and down in simple harmonic motion. The wave has a wavelength  , which is the distance between adjacent identical parts of the wave. The up and down disturbance of the surface propagates parallel to the surface at a speed  .

The water wave in the figure also has a length associated with it, called its wavelength , the distance between adjacent identical parts of a wave. (  is the distance parallel to the direction of propagation.) The speed of propagation  is the distance the wave travels in a given time, which is one wavelength in the time of one period. In equation form, that is



or



This fundamental relationship holds for all types of waves. For water waves,  is the speed of a surface wave; for sound,  is the speed of sound; and for visible light,  is the speed of light, for example.

# Take-Home Experiment: Waves in a Bowl

Fill a large bowl or basin with water and wait for the water to settle so there are no ripples. Gently drop a cork into the middle of the bowl. Estimate the wavelength and period of oscillation of the water wave that propagates away from the cork. Remove the cork from the bowl and wait for the water to settle again. Gently drop the cork at a height that is different from the first drop. Does the wavelength depend upon how high above the water the cork is dropped?# EXAMPLE 16.8

# Calculate the Velocity of Wave Propagation: Gull in the Ocean

Calculate the wave velocity of the ocean wave in Figure 16.28 if the distance between wave crests is  and the time for a sea gull to bob up and down is  .

# Strategy

We are asked to find  . The given information tells us that  and  . Therefore, we can use  to find the wave velocity.

# Solution

1. Enter the known values into  :



2. Solve for  to find 

# Discussion

This slow speed seems reasonable for an ocean wave. Note that the wave moves to the right in the figure at this speed, not the varying speed at which the sea gull moves up and down.

# Transverse and Longitudinal Waves

A simple wave consists of a periodic disturbance that propagates from one place to another. The wave in Figure 16.29 propagates in the horizontal direction while the surface is disturbed in the vertical direction. Such a wave is called a transverse wave or shear wave; in such a wave, the disturbance is perpendicular to the direction of propagation. In contrast, in a longitudinal wave or compressional wave, the disturbance is parallel to the direction of propagation. Figure 16.30 shows an example of a longitudinal wave. The size of the disturbance is its amplitude  and is completely independent of the speed of propagation  .

  
FIGURE 16.29 In this example of a transverse wave, the wave propagates horizontally, and the disturbance in the cord is in the vertical direction.

  
FIGURE 16.30 In this example of a longitudinal wave, the wave propagates horizontally, and the disturbance in the cord is also in the horizontal direction.

Waves may be transverse, longitudinal, or a combination of the two. (Water waves are actually a combination of transverse and longitudinal. The simplified water wave illustrated in Figure 16.28 shows no longitudinal motion of the bird.) The waves on the strings of musical instruments are transverse—so are electromagnetic waves, such as visible light.Sound waves in air and water are longitudinal. Their disturbances are periodic variations in pressure that are transmitted in fluids. Fluids do not have appreciable shear strength, and thus the sound waves in them must be longitudinal or compressional. Sound in solids can be both longitudinal and transverse.

  
FIGURE 16.31 The wave on a guitar string is transverse. The sound wave rattles a sheet of paper in a direction that shows the sound wave is longitudinal.

Earthquake waves under Earth’s surface also have both longitudinal and transverse components (called compressional or P-waves and shear or S-waves, respectively). These components have important individual characteristics—they propagate at different speeds, for example. Earthquakes also have surface waves that are similar to surface waves on water.

# CHECK YOUR UNDERSTANDING

Why is it important to differentiate between longitudinal and transverse waves?

# Solution

In the different types of waves, energy can propagate in a different direction relative to the motion of the wave. This is important to understand how different types of waves affect the materials around them.

# PHET EXPLORATIONS

# Wave on a String

Watch a string vibrate in slow motion. Wiggle the end of the string and make waves, or adjust the frequency and amplitude of an oscillator. Adjust the damping and tension. The end can be fixed, loose, or open.

Click to view content (https://openstax.org/books/college-physics-2e/pages/16-9-waves)

# 16.10 Superposition and Interference

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Explain standing waves.   
Describe the mathematical representation of overtones and beat frequency.  
FIGURE 16.32 These waves result from the superposition of several waves from different sources, producing a complex pattern. (credit: waterborough, Wikimedia Commons)

Most waves do not look very simple. They look more like the waves in Figure 16.32 than like the simple water wave considered in Waves. (Simple waves may be created by a simple harmonic oscillation, and thus have a sinusoidal shape). Complex waves are more interesting, even beautiful, but they look formidable. Most waves appear complex because they result from several simple waves adding together. Luckily, the rules for adding waves are quite simple.

When two or more waves arrive at the same point, they superimpose themselves on one another. More specifically, the disturbances of waves are superimposed when they come together—a phenomenon called superposition. Each disturbance corresponds to a force, and forces add. If the disturbances are along the same line, then the resulting wave is a simple addition of the disturbances of the individual waves—that is, their amplitudes add. Figure 16.33 and Figure 16.34 illustrate superposition in two special cases, both of which produce simple results.

Figure 16.33 shows two identical waves that arrive at the same point exactly in phase. The crests of the two waves are precisely aligned, as are the troughs. This superposition produces pure constructive interference. Because the disturbances add, pure constructive interference produces a wave that has twice the amplitude of the individual waves, but has the same wavelength.

Figure 16.34 shows two identical waves that arrive exactly out of phase—that is, precisely aligned crest to trough—producing pure destructive interference. Because the disturbances are in the opposite direction for this superposition, the resulting amplitude is zero for pure destructive interference—the waves completely cancel.

  
FIGURE 16.33 Pure constructive interference of two identical waves produces one with twice the amplitude, but the same wavelength.  
FIGURE 16.34 Pure destructive interference of two identical waves produces zero amplitude, or complete cancellation.

While pure constructive and pure destructive interference do occur, they require precisely aligned identical waves. The superposition of most waves produces a combination of constructive and destructive interference and can vary from place to place and time to time. Sound from a stereo, for example, can be loud in one spot and quiet in another. Varying loudness means the sound waves add partially constructively and partially destructively at different locations. A stereo has at least two speakers creating sound waves, and waves can reflect from walls. All these waves superimpose. An example of sounds that vary over time from constructive to destructive is found in the combined whine of airplane jets heard by a stationary passenger. The combined sound can fluctuate up and down in volume as the sound from the two engines varies in time from constructive to destructive. These examples are of waves that are similar.

An example of the superposition of two dissimilar waves is shown in Figure 16.35. Here again, the disturbances add and subtract, producing a more complicated looking wave.

  
FIGURE 16.35 Superposition of non-identical waves exhibits both constructive and destructive interference.

# Standing Waves

Sometimes waves do not seem to move; rather, they just vibrate in place. Unmoving waves can be seen on the surface of a glass of milk in a refrigerator, for example. Vibrations from the refrigerator motor create waves on the milk that oscillate up and down but do not seem to move across the surface. These waves are formed by the superposition of two or more moving waves, such as illustrated in Figure 16.36 for two identical waves moving in opposite directions. The waves move through each other with their disturbances adding as they go by. If the two waves have the same amplitude and wavelength, then they alternate between constructive and destructive interference. The resultant looks like a wave standing in place and, thus, is called a standing wave. Waves on the glass of milk are one example of standing waves. There are other standing waves, such as on guitar strings and in organ pipes. With the glass of milk, the two waves that produce standing waves may come from reflections from the side of the glass.

A closer look at earthquakes provides evidence for conditions appropriate for resonance, standing waves, and constructive and destructive interference. A building may be vibrated for several seconds with a driving frequency matching that of the natural frequency of vibration of the building—producing a resonance resulting in one buildingcollapsing while neighboring buildings do not. Often buildings of a certain height are devastated while other taller buildings remain intact. The building height matches the condition for setting up a standing wave for that particular height. As the earthquake waves travel along the surface of Earth and reflect off denser rocks, constructive interference occurs at certain points. Often areas closer to the epicenter are not damaged while areas farther away are damaged.

  
FIGURE 16.36 Standing wave created by the superposition of two identical waves moving in opposite directions. The oscillations are at fixed locations in space and result from alternately constructive and destructive interference.

Standing waves are also found on the strings of musical instruments and are due to reflections of waves from the ends of the string. Figure 16.37 and Figure 16.38 show three standing waves that can be created on a string that is fixed at both ends. Nodes are the points where the string does not move; more generally, nodes are where the wave disturbance is zero in a standing wave. The fixed ends of strings must be nodes, too, because the string cannot move there. The word antinode is used to denote the location of maximum amplitude in standing waves. Standing waves on strings have a frequency that is related to the propagation speed  of the disturbance on the string. The wavelength  is determined by the distance between the points where the string is fixed in place.

The lowest frequency, called the fundamental frequency, is thus for the longest wavelength, which is seen to be  . Therefore, the fundamental frequency is  . In this case, the overtones or harmonics are multiples of the fundamental frequency. As seen in Figure 16.38, the first harmonic can easily be calculated since  . Thus,  . Similarly,  , and so on. All of these frequencies can be changed by adjusting the tension in the string. The greater the tension, the greater  is and the higher the frequencies. This observation is familiar to anyone who has ever observed a string instrument being tuned. We will see in later chapters that standing waves are crucial to many resonance phenomena, such as in sounding boxes on string instruments.

  
FIGURE 16.37 The figure shows a string oscillating at its fundamental frequency.   
FIGURE 16.38 First and second overtones are shown.

# Beats

Striking two adjacent keys on a piano produces a warbling combination usually considered to be unpleasant. The superposition of two waves of similar but not identical frequencies is the culprit. Another example is often noticeable in jet aircraft, particularly the two-engine variety, while taxiing. The combined sound of the engines goes up and down in loudness. This varying loudness happens because the sound waves have similar but not identical frequencies. The discordant warbling of the piano and the fluctuating loudness of the jet engine noise are both due to alternately constructive and destructive interference as the two waves go in and out of phase. Figure 16.39 illustrates this graphically.

  
FIGURE 16.39 Beats are produced by the superposition of two waves of slightly different frequencies but identical amplitudes. The waves alternate in time between constructive interference and destructive interference, giving the resulting wave a time-varying amplitude.

The wave resulting from the superposition of two similar-frequency waves has a frequency that is the average of the two. This wave fluctuates in amplitude, or beats, with a frequency called the beat frequency. We can determine the beat frequency by adding two waves together mathematically. Note that a wave can be represented at one point in space as

where  is the frequency of the wave. Adding two waves that have different frequencies but identical amplitudes produces a resultant



More specifically,



Using a trigonometric identity, it can be shown that



where



is the beat frequency, and  is the average of  and  . These results mean that the resultant wave has twice the amplitude and the average frequency of the two superimposed waves, but it also fluctuates in overall amplitude at the beat frequency  . The first cosine term in the expression effectively causes the amplitude to go up and down. The second cosine term is the wave with frequency  . This result is valid for all types of waves. However, if it is a sound wave, providing the two frequencies are similar, then what we hear is an average frequency that gets louder and softer (or warbles) at the beat frequency.

# Making Career Connections

Piano tuners use beats routinely in their work. When comparing a note with a tuning fork, they listen for beats and adjust the string until the beats go away (to zero frequency). For example, if the tuning fork has a  frequency and two beats per second are heard, then the other frequency is either or  . Most keys hit multiple strings, and these strings are actually adjusted until they have nearly the same frequency and give a slow beat for richness. Twelve-string guitars and mandolins are also tuned using beats.

While beats may sometimes be annoying in audible sounds, we will find that beats have many applications. Observing beats is a very useful way to compare similar frequencies. There are applications of beats as apparently disparate as in ultrasonic imaging and radar speed traps.

# CHECK YOUR UNDERSTANDING

Imagine you are holding one end of a jump rope, and your friend holds the other. If your friend holds her end still, you can move your end up and down, creating a transverse wave. If your friend then begins to move her end up and down, generating a wave in the opposite direction, what resultant wave forms would you expect to see in the jump rope?

# Solution

The rope would alternate between having waves with amplitudes two times the original amplitude and reaching equilibrium with no amplitude at all. The wavelengths will result in both constructive and destructive interference

# CHECK YOUR UNDERSTANDING

Define nodes and antinodes.

# Solution

Nodes are areas of wave interference where there is no motion. Antinodes are areas of wave interference where the motion is at its maximum point.

# CHECK YOUR UNDERSTANDING

You hook up a stereo system. When you test the system, you notice that in one corner of the room, the sounds seemdull. In another area, the sounds seem excessively loud. Describe how the sound moving about the room could result in these effects.

# Solution

With multiple speakers putting out sounds into the room, and these sounds bouncing off walls, there is bound to be some wave interference. In the dull areas, the interference is probably mostly destructive. In the louder areas, the interference is probably mostly constructive.

# PHET EXPLORATIONS

# Wave Interference

Make waves with a dripping faucet, audio speaker, or laser! Add a second source or a pair of slits to create an interference pattern.

Click to view content (https://openstax.org/books/college-physics-2e/pages/16-10-superposition-andinterference)

# 16.11 Energy in Waves: Intensity

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

• Calculate the intensity and the power of rays and waves.

  
FIGURE 16.40 The destructive effect of an earthquake is palpable evidence of the energy carried in these waves. The Richter scale rating of earthquakes is related to both their amplitude and the energy they carry. (credit: Petty Officer 2nd Class Candice Villarreal, U.S. Navy)

All waves carry energy. The energy of some waves can be directly observed. Earthquakes can shake whole cities to the ground, performing the work of thousands of wrecking balls.

Loud sounds pulverize nerve cells in the inner ear, causing permanent hearing loss. Ultrasound is used for deep-heat treatment of muscle strains. A laser beam can burn away a malignancy. Water waves chew up beaches.

The amount of energy in a wave is related to its amplitude. Large-amplitude earthquakes produce large ground displacements. Loud sounds have higher pressure amplitudes and come from larger-amplitude source vibrations than soft sounds. Large ocean breakers churn up the shore more than small ones. More quantitatively, a wave is a displacement that is resisted by a restoring force. The larger the displacement  , the larger the force  needed to create it. Because work  is related to force multiplied by distance  and energy is put into the wave by the work done to create it, the energy in a wave is related to amplitude. In fact, a wave’s energy is directly proportional to its amplitude squared because



The energy effects of a wave depend on time as well as amplitude. For example, the longer deep-heat ultrasound is applied, the more energy it transfers. Waves can also be concentrated or spread out. Sunlight, for example, can befocused to burn wood. Earthquakes spread out, so they do less damage the farther they get from the source. In both cases, changing the area the waves cover has important effects. All these pertinent factors are included in the definition of intensity  as power per unit area:



where  is the power carried by the wave through area  . The definition of intensity is valid for any energy in transit, including that carried by waves. The SI unit for intensity is watts per square meter  ). For example, infrared and visible energy from the Sun impinge on Earth at an intensity of  just above the atmosphere. There are other intensity-related units in use, too. The most common is the decibel. For example, a 90 decibel sound level corresponds to an intensity of  . (This quantity is not much power per unit area considering that 90 decibels is a relatively high sound level. Decibels will be discussed in some detail in a later chapter.

# EXAMPLE 16.9

# Calculating intensity and power: How much energy is in a ray of sunlight?

The average intensity of sunlight on Earth’s surface is about  .

(a) Calculate the amount of energy that falls on a solar collector having an area of  in  .

(b) What intensity would such sunlight have if concentrated by a magnifying glass onto an area 200 times smaller than its own?

# Strategy a

Because power is energy per unit time or  , the definition of intensity can be written as  , and this equation can be solved for E with the given information.

# Solution a

1. Begin with the equation that states the definition of intensity:



2. Replace  with its equivalent  :



3. Solve for  :



4. Substitute known values into the equation:



5. Calculate to find  and convert units:



# Discussion a

The energy falling on the solar collector in  in part is enough to be useful—for example, for heating a significant amount of water.

# Strategy b

Taking a ratio of new intensity to old intensity and using primes for the new quantities, we will find that it depends on the ratio of the areas. All other quantities will cancel.

# Solution b

1. Take the ratio of intensities, which yields:

2. Identify the knowns:



3. Substitute known quantities:



4. Calculate to find  :



# Discussion b

Decreasing the area increases the intensity considerably. The intensity of the concentrated sunlight could even start a fire.

# EXAMPLE 16.10

# Determine the combined intensity of two waves: Perfect constructive interference

If two identical waves are spatially separated, each having an intensity of  , interfere perfectly constructively in a particular location, what is the intensity of the wave at this particular location?

# Strategy

We know from Superposition and Interference that when two identical waves, which have equal amplitudes  , interfere perfectly constructively, the resulting wave has an amplitude of  . Because a wave’s intensity is proportional to amplitude squared, the intensity of the resulting wave is four times as great as in the individual waves.

# Solution

1. Recall that intensity is proportional to amplitude squared.

2. Calculate the new amplitude:



3. Recall that the intensity of the old amplitude was:



4. Take the ratio of new intensity to the old intensity. This gives:



5. Calculate to find  :



# Discussion

The intensity goes up by a factor of 4 when the amplitude doubles. This answer is a little disquieting. The two individual waves each have intensities of  , yet their sum has an intensity of  , which may appear to violate conservation of energy. This violation, of course, cannot happen. What does happen is intriguing. The area over which the intensity is  is much less than the area covered by the two waves before they interfered. There are other areas where the intensity is zero. The addition of waves is not as simple as our first look in Superposition and Interference suggested. We actually get a pattern of both constructive interference anddestructive interference whenever two waves are added. For example, if we have two stereo speakers putting out  each, there will be places in the room where the intensity is  , other places where the intensity is zero, and others in between. Figure 16.41 shows what this interference might look like. We will pursue interference patterns elsewhere in this text.

  
FIGURE 16.41 These stereo speakers produce both constructive interference and destructive interference in the room, a property common to the superposition of all types of waves. The shading is proportional to intensity.

# CHECK YOUR UNDERSTANDING

Which measurement of a wave is most important when determining the wave's intensity?

# Solution

Amplitude, because a wave’s energy is directly proportional to its amplitude squared.# Glossary

amplitude the maximum displacement from the equilibrium position of an object oscillating around the equilibrium position   
antinode the location of maximum amplitude in standing waves   
beat frequency the frequency of the amplitude fluctuations of a wave   
constructive interference when two waves arrive at the same point exactly in phase; that is, the crests of the two waves are precisely aligned, as are the troughs   
critical damping the condition in which the damping of an oscillator causes it to return as quickly as possible to its equilibrium position without oscillating back and forth about this position   
deformation displacement from equilibrium   
destructive interference when two identical waves arrive at the same point exactly out of phase; that is, precisely aligned crest to trough   
elastic potential energy potential energy stored as a result of deformation of an elastic object, such as the stretching of a spring   
force constant a constant related to the rigidity of a system: the larger the force constant, the more rigid the system; the force constant is represented by    
frequency number of events per unit of time   
fundamental frequency the lowest frequency of a periodic waveform   
intensity power per unit area   
longitudinal wave a wave in which the disturbance is parallel to the direction of propagation   
natural frequency the frequency at which a system would oscillate if there were no driving and no damping forces   
nodes the points where the string does not move; more generally, nodes are where the wave disturbance is zero in a standing wave   
oscillate moving back and forth regularly between two points   
over damping the condition in which damping of an oscillator causes it to return to equilibrium without oscillating; oscillator moves more slowly toward equilibrium than in the critically damped system   
overtones multiples of the fundamental frequency of a sound   
period time it takes to complete one oscillation   
periodic motion motion that repeats itself at regular time intervals   
resonance the phenomenon of driving a system with a frequency equal to the system's natural frequency   
resonate a system being driven at its natural frequency   
restoring force force acting in opposition to the force caused by a deformation   
simple harmonic motion the oscillatory motion in a system where the net force can be described by Hooke’s law   
simple harmonic oscillator a device that implements Hooke’s law, such as a mass that is attached to a spring, with the other end of the spring being connected to a rigid support such as a wall   
simple pendulum an object with a small mass suspended from a light wire or string   
superposition the phenomenon that occurs when two or more waves arrive at the same point   
transverse wave a wave in which the disturbance is perpendicular to the direction of propagation   
under damping the condition in which damping of an oscillator causes it to return to equilibrium with the amplitude gradually decreasing to zero; system returns to equilibrium faster but overshoots and crosses the equilibrium position one or more times   
wave a disturbance that moves from its source and carries energy   
wave velocity the speed at which the disturbance moves. Also called the propagation velocity or propagation speed   
wavelength the distance between adjacent identical parts of a wave

# Section Summary

# 16.1 Hooke’s Law: Stress and Strain Revisited

• An oscillation is a back and forth motion of an object between two points of deformation. An oscillation may create a wave, which is a disturbance that propagates from where it was created. The simplest type of oscillations and waves are related to systems that can be described by

Hooke’s law:   
 .   
where  is the restoring force,  is the   
displacement from equilibrium or deformation, and  is the force constant of the system.   
Elastic potential energy  stored in the   
deformation of a system that can be described by Hooke’s law is given by   
# 16.2 Period and Frequency in Oscillations

• Periodic motion is a repetitious oscillation.   
• The time for one oscillation is the period  .   
The number of oscillations per unit time is the frequency  .   
• These quantities are related by 

# 16.3 Simple Harmonic Motion: A Special Periodic Motion

• Simple harmonic motion is oscillatory motion for a system that can be described only by Hooke’s law. Such a system is also called a simple harmonic oscillator. Maximum displacement is the amplitude  . The period  and frequency  of a simple harmonic oscillator are given by  and  , where  is the mass of the system.   
• Displacement in simple harmonic motion as a function of time is given by  cos    
• The velocity is given by  where  .   
• The acceleration is found to be  cos 

# 16.4 The Simple Pendulum

• A mass suspended by a wire of length  is a simple pendulum and undergoes simple harmonic motion for amplitudes less than about  . The period of a simple pendulum is  where  is the length of the string and  is the acceleration due to gravity.

# 16.5 Energy and the Simple Harmonic Oscillator

Energy in the simple harmonic oscillator is shared   
between elastic potential energy and kinetic   
energy, with the total being constant:   
   
Maximum velocity depends on three factors: it is   
directly proportional to amplitude, it is greater for   
stiffer systems, and it is smaller for objects that   
have larger masses:   


# 16.6 Uniform Circular Motion and Simple Harmonic Motion

A projection of uniform circular motion undergoes simple harmonic oscillation.

# 16.7 Damped Harmonic Motion

• Damped harmonic oscillators have nonconservative forces that dissipate their energy. Critical damping returns the system to equilibrium as fast as possible without overshooting. An underdamped system will oscillate through the equilibrium position. An overdamped system moves more slowly toward equilibrium than one that is critically damped.

# 16.8 Forced Oscillations and Resonance

• A system’s natural frequency is the frequency at which the system will oscillate if not affected by driving or damping forces. A periodic force driving a harmonic oscillator at its natural frequency produces resonance. The system is said to resonate. The less damping a system has, the higher the amplitude of the forced oscillations near resonance. The more damping a system has, the broader response it has to varying driving frequencies.

# 16.9 Waves

• A wave is a disturbance that moves from the point of creation with a wave velocity  . • A wave has a wavelength  , which is the distance between adjacent identical parts of the wave. Wave velocity and wavelength are related to the wave’s frequency and period by  or  A transverse wave has a disturbance perpendicular to its direction of propagation, whereas a longitudinal wave has a disturbance parallel to its direction of propagation.

# 16.10 Superposition and Interference

• Superposition is the combination of two waves at the same location. Constructive interference occurs when two identical waves are superimposed in phase. Destructive interference occurs when two identical waves are superimposed exactly out of phase. A standing wave is one in which two waves superimpose to produce a wave that varies in amplitude but does not propagate.   
• Nodes are points of no motion in standing waves.• An antinode is the location of maximum amplitude of a standing wave. Waves on a string are resonant standing waves with a fundamental frequency and can occur at higher multiples of the fundamental, called overtones or harmonics. Beats occur when waves of similar frequencies  and  are superimposed. The resulting amplitude oscillates with a beat frequency given by 

# 16.11 Energy in Waves: Intensity

Intensity is defined to be the power per unit area:  and has units of  .

# Conceptual Questions

# 16.1 Hooke’s Law: Stress and Strain Revisited

1. Describe a system in which elastic potential energy is stored.

# 16.3 Simple Harmonic Motion: A Special Periodic Motion

2. What conditions must be met to produce simple harmonic motion?   
3. (a) If frequency is not constant for some oscillation, can the oscillation be simple harmonic motion? (b) Can you think of any examples of harmonic motion where the frequency may depend on the amplitude?   
4. Give an example of a simple harmonic oscillator, specifically noting how its frequency is independent of amplitude.   
5. Explain why you expect an object made of a stiff material to vibrate at a higher frequency than a similar object made of a spongy material.   
6. As you pass a freight truck with a trailer on a highway, you notice that its trailer is bouncing up and down slowly. Is it more likely that the trailer is heavily loaded or nearly empty? Explain your answer.   
7. Some people modify cars to be much closer to the ground than when manufactured. Should they install stiffer springs? Explain your answer.

# 16.4 The Simple Pendulum

8. Pendulum clocks are made to run at the correct rate by adjusting the pendulum’s length. Suppose you move from one city to another where the acceleration due to gravity is slightly greater, taking your pendulum clock with you, will you have to lengthen or shorten the pendulum to keep the correct time, other factors remaining constant? Explain your answer.

# 16.5 Energy and the Simple Harmonic Oscillator

9. Explain in terms of energy how dissipative forces such as friction reduce the amplitude of a harmonic oscillator. Also explain how a driving mechanism can compensate. (A pendulum clock is such a system.)

# 16.7 Damped Harmonic Motion

10. Give an example of a damped harmonic oscillator. (They are more common than undamped or simple harmonic oscillators.)

11. How would a car bounce after a bump under each of these conditions?

• overdamping • underdamping • critical damping

12. Most harmonic oscillators are damped and, if undriven, eventually come to a stop. How is this observation related to the second law of thermodynamics?

# 16.8 Forced Oscillations and Resonance

13. Why are soldiers in general ordered to “route step” (walk out of step) across a bridge?

# 16.9 Waves

14. Give one example of a transverse wave and another of a longitudinal wave, being careful to note the relative directions of the disturbance and wave propagation in each.   
15. What is the difference between propagation speed and the frequency of a wave? Does one or both affect wavelength? If so, how?# 16.10 Superposition and Interference

16. Speakers in stereo systems have two color-coded terminals to indicate how to hook up the wires. If the wires are reversed, the speaker moves in a direction opposite that of a properly connected speaker. Explain why it is important to have both speakers connected the same way.

# 16.11 Energy in Waves: Intensity

17. Two identical waves undergo pure constructive interference. Is the resultant intensity twice that of the individual waves? Explain your answer.   
18. Circular water waves decrease in amplitude as they move away from where a rock is dropped. Explain why.

# Problems & Exercises

# 16.1 Hooke’s Law: Stress and Strain Revisited

1. Fish are hung on a spring scale to determine their mass (most fishermen feel no obligation to truthfully report the mass). (a) What is the force constant of the spring in such a scale if it the spring stretches  for a  load? (b) What is the mass of a fish that stretches the spring  (c) How far apart are the half-kilogram marks on the scale?   
2. It is weigh-in time for the local under-85-kg rugby team. The bathroom scale used to assess eligibility can be described by Hooke’s law and is depressed  by its maximum load of $ 1 2 0 \ k \underline { { \sf s } } .$ (a) What is the spring’s effective spring constant? (b) A player stands on the scales and depresses it by  . Is he eligible to play on this under-  team?   
3. One type of BB gun uses a spring-driven plunger to blow the BB from its barrel. (a) Calculate the force constant of its plunger’s spring if you must compress it  to drive the  plunger to a top speed of  . (b) What force must be exerted to compress the spring?   
4. (a) The springs of a pickup truck act like a single spring with a force constant of  . By how much will the truck be depressed by its maximum load of  (b) If the pickup truck has four identical springs, what is the force constant of each?   
5. When an  man stands on a pogo stick, the spring is compressed  . (a) What is the force constant of the spring? (b) Will the spring be compressed more when he hops down the road?   
6. A spring has a length of  when a  mass hangs from it, and a length of  when a 1.95-kg mass hangs from it. (a) What is the force constant of the spring? (b) What is the unloaded length of the spring?

# 16.2 Period and Frequency in Oscillations

7. What is the period of  electrical power?   
8. If your heart rate is 150 beats per minute during strenuous exercise, what is the time per beat in units of seconds?   
9. Find the frequency of a tuning fork that takes  to complete one oscillation.   
10. A stroboscope is set to flash every  . What is the frequency of the flashes?   
11. A tire has a tread pattern with a crevice every 2.00 cm. Each crevice makes a single vibration as the tire moves. What is the frequency of these vibrations if the car moves at    
12. Engineering Application Each piston of an engine makes a sharp sound every other revolution of the engine. (a) How fast is a race car going if its eight-cylinder engine emits a sound of frequency  , given that the engine makes 2000 revolutions per kilometer? (b) At how many revolutions per minute is the engine rotating?

# 16.3 Simple Harmonic Motion: A Special Periodic Motion

13. A type of cuckoo clock keeps time by having a mass bouncing on a spring, usually something cute like a cherub in a chair. What force constant is needed to produce a period of 0.500 s for a 0.0150-kg mass?   
14. If the spring constant of a simple harmonic oscillator is doubled, by what factor will the mass of the system need to change in order for the frequency of the motion to remain the same?   
15. A 0.500-kg mass suspended from a spring oscillates with a period of 1.50 s. How much mass must be added to the object to change the period to 2.00 s?   
16. By how much leeway (both percentage and mass) would you have in the selection of the mass of the object in the previous problem if you did not wish the new period to be greater than 2.01 s or less than 1.99 s?17. Suppose you attach the object with mass to a vertical spring originally at rest, and let it bounce up and down. You release the object from rest at the spring’s original rest length. (a) Show that the spring exerts an upward force of on the object at its lowest point. (b) If the spring has a force constant of  and a  -mass object is set in motion as described, find the amplitude of the oscillations. (c) Find the maximum velocity.

18. A diver on a diving board is undergoing simple harmonic motion. Her mass is  and the period of her motion is 0.800 s. The next diver is a male whose period of simple harmonic oscillation is  . What is his mass if the mass of the board is negligible?

21. A  skydiver hanging from a parachute bounces up and down with a period of  . What is the new period of oscillation when a second skydiver, whose mass is  , hangs from the legs of the first, as seen in Figure 16.43.

19. Suppose a diving board with no one on it bounces up and down in a simple harmonic motion with a frequency of  . The board has an effective mass of  . What is the frequency of the simple harmonic motion of a  diver on the board?

  
FIGURE 16.43 The oscillations of one skydiver are about to be affected by a second skydiver. (credit: U.S. Army, www.army.mil)

# 16.4 The Simple Pendulum

As usual, the acceleration due to gravity in these problems is taken to be  , unless otherwise specified.

  
FIGURE 16.42 This child’s toy relies on springs to keep infants entertained. (credit: By Humboldthead, Flickr)

22. What is the length of a pendulum that has a period of 0.500 s?   
23. Some people think a pendulum with a period of 1.00 s can be driven with “mental energy” or psycho kinetically, because its period is the same as an average heartbeat. True or not, what is the length of such a pendulum?   
24. What is the period of a 1.00-m-long pendulum?   
25. How long does it take a child on a swing to complete one swing if her center of gravity is 4.00 m below the pivot?   
26. The pendulum on a cuckoo clock is 5.00 cm long. What is its frequency?   
27. Two parakeets sit on a swing with their combined center of mass 10.0 cm below the pivot. At what frequency do they swing?   
28. (a) A pendulum that has a period of 3.00000 s and that is located where the acceleration due to gravity is  is moved to a location where the acceleration due to gravity is  . What is its new period? (b) Explain why so many digits are needed in the value for the period, based on the relation between the period and the acceleration due to gravity. The device pictured in Figure 16.42 entertains infants while keeping them from wandering. The child bounces in a harness suspended from a door frame by a spring constant.   
(a) If the spring stretches  while   
supporting an  child, what is its spring   
constant?   
(b) What is the time for one complete bounce of this child? (c) What is the child’s maximum   
velocity if the amplitude of her bounce is 29. A pendulum with a period of 2.00000 s in one location  is moved to a new location where the period is now 1.99796 s. What is the acceleration due to gravity at its new location?   
30. (a) What is the effect on the period of a pendulum if you double its length? (b) What is the effect on the period of a pendulum if you decrease its length by    
31. Find the ratio of the new/old periods of a pendulum if the pendulum were transported from Earth to the Moon, where the acceleration due to gravity is  .   
32. At what rate will a pendulum clock run on the Moon, where the acceleration due to gravity is  , if it keeps time accurately on Earth? That is, find the time (in hours) it takes the clock’s hour hand to make one revolution on the Moon.   
33. Suppose the length of a clock’s pendulum is changed by  , exactly at noon one day. What time will it read 24.00 hours later, assuming it the pendulum has kept perfect time before the change? Note that there are two answers, and perform the calculation to four-digit precision.   
34. If a pendulum-driven clock gains  , what fractional change in pendulum length must be made for it to keep perfect time?

# 16.5 Energy and the Simple Harmonic Oscillator

35. The length of nylon rope from which a mountain climber is suspended has a force constant of  (a) What is the frequency at which he bounces, given his mass plus and the mass of his equipment are  Ignore the change in gravitational potential energy after the cord begins to stretch. (b) How much would this rope stretch to break the climber’s fall if he free-falls  before the rope runs out of slack? Hint: Use conservation of energy. (c) Repeat both parts of this problem in the situation where twice this length of nylon rope is used.

36. Engineering Application Near the top of the Citigroup Center building in New York City, there is an object with mass of  on springs that have adjustable force constants. Its function is to dampen winddriven oscillations of the building by oscillating at the same frequency as the building is being driven—the driving force is transferred to the object, which oscillates instead of the entire building. (a) What effective force constant should the springs have to make the object oscillate with a period of 2.00 s? (b) What energy is stored in the springs for a  displacement from equilibrium?

# 16.6 Uniform Circular Motion and Simple Harmonic Motion

37. (a)What is the maximum velocity of an  person bouncing on a bathroom scale having a force constant of  , if the amplitude of the bounce is  (b)What is the maximum energy stored in the spring?   
38. A novelty clock has  mass object bouncing on a spring that has a force constant of  . What is the maximum velocity of the object if the object bounces 3.00 cm above and below its equilibrium position? (b) How many joules of kinetic energy does the object have at its maximum velocity?   
39. At what positions is the speed of a simple harmonic oscillator half its maximum? That is, what values of  give  , where  is the amplitude of the motion?   
40. A ladybug sits  from the center of a Beatles music album spinning at 33.33 rpm. What is the maximum velocity of its shadow on the wall behind the turntable, if illuminated parallel to the record by the parallel rays of the setting Sun?

# 16.7 Damped Harmonic Motion

41. The amplitude of a lightly damped oscillator decreases by  during each cycle. What percentage of the mechanical energy of the oscillator is lost in each cycle?

# 16.8 Forced Oscillations and Resonance

42. How much energy must the shock absorbers of a  car dissipate in order to damp a bounce that initially has a velocity of  at the equilibrium position? Assume the car returns to its original vertical position.43. If a car has a suspension system with a force constant of  , how much energy must the car’s shocks remove to dampen an oscillation starting with a maximum displacement of 

44. (a) How much will a spring that has a force constant of  be stretched by an object with a mass of  when hung motionless from the spring? (b) Calculate the decrease in gravitational potential energy of the  object when it descends this distance. (c) Part of this gravitational energy goes into the spring. Calculate the energy stored in the spring by this stretch, and compare it with the gravitational potential energy. Explain where the rest of the energy might go.

45. Suppose you have a  object on a horizontal surface connected to a spring that has a force constant of  . There is simple friction between the object and surface with a static coefficient of friction  . (a) How far can the spring be stretched without moving the mass? (b) If the object is set into oscillation with an amplitude twice the distance found in part (a), and the kinetic coefficient of friction is  , what total distance does it travel before stopping? Assume it starts at the maximum amplitude.

46. Engineering Application: A suspension bridge oscillates with an effective force constant of  (a) How much energy is needed to make it oscillate with an amplitude of  (b) If soldiers march across the bridge with a cadence equal to the bridge’s natural frequency and impart  of energy each second, how long does it take for the bridge’s oscillations to go from  to  amplitude?

51. Scouts at a camp shake the rope bridge they have just crossed and observe the wave crests to be  apart. If they shake the bridge twice per second, what is the propagation speed of the waves?

52. What is the wavelength of the waves you create in a swimming pool if you splash your hand at a rate of  and the waves propagate at 

53. What is the wavelength of an earthquake that shakes you with a frequency of  and gets to another city  away in 

54. Radio waves transmitted through space at  by the Voyager spacecraft have a wavelength of  . What is their frequency?

55. Your ear is capable of differentiating sounds that arrive at the ear just 1.00 ms apart. What is the minimum distance between two speakers that produce sounds that arrive at noticeably different times on a day when the speed of sound is  s?

56. (a) Seismographs measure the arrival times of earthquakes with a precision of 0.100 s. To get the distance to the epicenter of the quake, they compare the arrival times of S- and P-waves, which travel at different speeds. Figure 16.44) If S- and P-waves travel at 4.00 and  , respectively, in the region considered, how precisely can the distance to the source of the earthquake be determined? (b) Seismic waves from underground detonations of nuclear bombs can be used to locate the test site and detect violations of test bans. Discuss whether your answer to (a) implies a serious limit to such detection. (Note also that the uncertainty is greater if there is an uncertainty in the propagation speeds of the S- and P-waves.)

# 16.9 Waves

47. Storms in the South Pacific can create waves that travel all the way to the California coast, which are  away. How long does it take them if they travel at    
48. Waves on a swimming pool propagate at  s. You splash the water at one end of the pool and observe the wave go to the opposite end, reflect, and return in  . How far away is the other end of the pool?   
49. Wind gusts create ripples on the ocean that have a wavelength of  and propagate at  . What is their frequency?   
50. How many times a minute does a boat bob up and down on ocean waves that have a wavelength of  and a propagation speed of 

  
FIGURE 16.44 A seismograph as described in above problem.(credit: Oleg Alexandrov)# 16.10 Superposition and Interference

57. A car has two horns, one emitting a frequency of  and the other emitting a frequency of 203 Hz. What beat frequency do they produce?

58. The middle-C hammer of a piano hits two strings, producing beats of  . One of the strings is tuned to  . What frequencies could the other string have?

59. Two tuning forks having frequencies of 460 and  are struck simultaneously. What average frequency will you hear, and what will the beat frequency be?

60. Twin jet engines on an airplane are producing an average sound frequency of  with a beat frequency of  . What are their individual frequencies?

61. A wave traveling on a Slinky® that is stretched to 4 m takes  to travel the length of the Slinky and back again. (a) What is the speed of the wave? (b) Using the same Slinky stretched to the same length, a standing wave is created which consists of three antinodes and four nodes. At what frequency must the Slinky be oscillating?

62. Three adjacent keys on a piano (F, F-sharp, and G) are struck simultaneously, producing frequencies of 349, 370, and  . What beat frequencies are produced by this discordant combination?

# 16.11 Energy in Waves: Intensity

63. Medical Application

Ultrasound of intensity  is produced by the rectangular head of a medical imaging device measuring 3.00 by 5.00 cm. What is its power output?

64. The low-frequency speaker of a stereo set has a surface area of  and produces 1W of acoustical power. What is the intensity at the speaker? If the speaker projects sound uniformly in all directions, at what distance from the speaker is the intensity 

65. To increase intensity of a wave by a factor of 50, by what factor should the amplitude be increased?

66. Engineering Application A device called an insolation meter is used to measure the intensity of sunlight has an area of  and registers 6.50 W. What is the intensity in 

67. Astronomy Application Energy from the Sun arrives at the top of the Earth’s atmosphere with an intensity of  How long does it take for  to arrive on an area of 

68. Suppose you have a device that extracts energy from ocean breakers in direct proportion to their intensity. If the device produces  of power on a day when the breakers are  high, how much will it produce when they are  high?

69. Engineering Application (a) A photovoltaic array of (solar cells) is  efficient in gathering solar energy and converting it to electricity. If the average intensity of sunlight on one day is  what area should your array have to gather energy at the rate of 100 W? (b) What is the maximum cost of the array if it must pay for itself in two years of operation averaging 10.0 hours per day? Assume that it earns money at the rate of  per kilowatt-hour.

70. A microphone receiving a pure sound tone feeds an oscilloscope, producing a wave on its screen. If the sound intensity is originally  but is turned up until the amplitude increases by  , what is the new intensity?

71. Medical Application (a) What is the intensity in  of a laser beam used to burn away cancerous tissue that, when  absorbed, puts 500 J of energy into a circular spot  in diameter in  (b) Discuss how this intensity compares to the average intensity of sunlight (about  ) and the implications that would have if the laser beam entered your eye. Note how the amount of damage depends on the time duration of the exposure.