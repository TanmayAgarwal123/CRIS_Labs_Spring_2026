# Chapter 10 - Rotational Motion and Angular Momentum

  
FIGURE 10.1 The mention of a tornado conjures up images of raw destructive power. Tornadoes blow houses away as if they were made of paper and have been known to pierce tree trunks with pieces of straw. They descend from clouds in funnel-like shapes that spin violently, particularly at the bottom where they are most narrow, producing winds as high as  . (credit: Daphne Zaras, U.S. National Oceanic and Atmospheric Administration)

# CHAPTER OUTLINE

10.1 Angular Acceleration   
10.2 Kinematics of Rotational Motion   
10.3 Dynamics of Rotational Motion: Rotational Inertia   
10.4 Rotational Kinetic Energy: Work and Energy Revisited   
10.5 Angular Momentum and Its Conservation   
10.6 Collisions of Extended Bodies in Two Dimensions   
10.7 Gyroscopic Effects: Vector Aspects of Angular Momentum

INTRODUCTION TO ROTATIONAL MOTION AND ANGULAR MOMENTUM Why do tornadoes spin at all? And why do tornados spin so rapidly? The answer is that air masses that produce tornadoes are themselves rotating, and when the radii of the air masses decrease, their rate of rotation increases. An ice skater increases her spin in an exactly analogous manner as seen in Figure 10.2. The skater starts her rotation with outstretched limbs and increases her spin by pulling them in toward her body. The same physics describes the exhilarating spin of a skater and the wrenching force of a tornado.

Clearly, force, energy, and power are associated with rotational motion. These and other aspects of rotational motion are covered in this chapter. We shall see that all important aspects of rotational motion either have already been defined for linear motion or have exact analogs in linear motion. First, we look at angular acceleration—the rotational analog of linear acceleration.  
FIGURE 10.2 This figure skater increases her rate of spin by pulling her arms and her extended leg closer to her axis of rotation. (credit: Luu, Wikimedia Commons)

Click to view content (https://openstax.org/books/college-physics-2e/pages/10-introduction-to-rotational-motion  
and-angular-momentum)   
10.1 Angular Acceleration

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Describe uniform circular motion.   
Explain non-uniform circular motion.   
Calculate angular acceleration of an object.   
Observe the link between linear and angular acceleration.

Uniform Circular Motion and Gravitation discussed only uniform circular motion, which is motion in a circle at constant speed and, hence, constant angular velocity. Recall that angular velocity  was defined as the time rate of change of angle  :



where  is the angle of rotation as seen in Figure 10.3. The relationship between angular velocity  and linear velocity  was also defined in Rotation Angle and Angular Velocity as



or



where  is the radius of curvature, also seen in Figure  . According to the sign convention, the counter clockwise direction is considered as positive direction and clockwise direction as negative

  
FIGURE 10.3 This figure shows uniform circular motion and some of its defined quantities.Angular velocity is not constant when a skater pulls in her arms, when a child starts up a merry-go-round from rest, or when a computer’s hard disk slows to a halt when switched off. In all these cases, there is an angular acceleration, in which  changes. The faster the change occurs, the greater the angular acceleration. Angular acceleration  is defined as the rate of change of angular velocity. In equation form, angular acceleration is expressed as follows:



where  is the change in angular velocity and  is the change in time. The units of angular acceleration are  , or  . If  increases, then  is positive. If  decreases, then  is negative.

# EXAMPLE 10.1

# Calculating the Angular Acceleration and Deceleration of a Bike Wheel

Suppose a teenager puts her bicycle on its back and starts the rear wheel spinning from rest to a final angular velocity of 250 rpm in  . (a) Calculate the angular acceleration in  . (b) If she now slams on the brakes, causing an angular acceleration of  , how long does it take the wheel to stop?

# Strategy for (a)

The angular acceleration can be found directly from its definition in  because the final angular velocity and time are given. We see that  is 250 rpm and  is  .

# Solution for (a)

Entering known information into the definition of angular acceleration, we get



Because  is in revolutions per minute (rpm) and we want the standard units of  for angular acceleration, we need to convert  from rpm to rad/s:



Entering this quantity into the expression for  , we get



# Strategy for (b)

In this part, we know the angular acceleration and the initial angular velocity. We can find the stoppage time by using the definition of angular acceleration and solving for  , yielding



# Solution for (b)

Here the angular velocity decreases from (250 rpm) to zero, so that  is , and  is given to  . Thus,

# Discussion

Note that the angular acceleration as the girl spins the wheel is small and positive; it takes 5 s to produce an appreciable angular velocity. When she hits the brake, the angular acceleration is large and negative. The angular velocity quickly goes to zero. In both cases, the relationships are analogous to what happens with linear motion. For example, there is a large deceleration when you crash into a brick wall—the velocity change is large in a short time interval.

If the bicycle in the preceding example had been on its wheels instead of upside-down, it would first have accelerated along the ground and then come to a stop. This connection between circular motion and linear motion needs to be explored. For example, it would be useful to know how linear and angular acceleration are related. In circular motion, linear acceleration is tangent to the circle at the point of interest, as seen in Figure 10.4. Thus, linear acceleration is called tangential acceleration  .

  
FIGURE 10.4 In circular motion, linear acceleration  , occurs as the magnitude of the velocity changes:  is tangent to the motion. In the context of circular motion, linear acceleration is also called tangential acceleration  .

Linear or tangential acceleration refers to changes in the magnitude of velocity but not its direction. We know from Uniform Circular Motion and Gravitation that in circular motion centripetal acceleration,  , refers to changes in the direction of the velocity but not its magnitude. An object undergoing circular motion experiences centripetal acceleration, as seen in Figure 10.5. Thus,  and  are perpendicular and independent of one another. Tangential acceleration  is directly related to the angular acceleration  and is linked to an increase or decrease in the velocity, but not its direction.

  
FIGURE 10.5 Centripetal acceleration  occurs as the direction of velocity changes; it is perpendicular to the circular motion. Centripetal and tangential acceleration are thus perpendicular to each other.

Now we can find the exact relationship between linear acceleration  and angular acceleration . Because linear acceleration is proportional to a change in the magnitude of the velocity, it is defined (as it was in One-Dimensional# Kinematics) to be



For circular motion, note that  , so that



The radius  is constant for circular motion, and so  . Thus,



By definition,  . Thus,



or



These equations mean that linear acceleration and angular acceleration are directly proportional. The greater the angular acceleration is, the larger the linear (tangential) acceleration is, and vice versa. For example, the greater the angular acceleration of a car’s drive wheels, the greater the acceleration of the car. The radius also matters. For example, the smaller a wheel, the smaller its linear acceleration for a given angular acceleration  .

# EXAMPLE 10.2

# Calculating the Angular Acceleration of a Motorcycle Wheel

A powerful motorcycle can accelerate from 0 to  (about  in  . What is the angular acceleration of its  -radius wheels? (See Figure  )

  
FIGURE 10.6 The linear acceleration of a motorcycle is accompanied by an angular acceleration of its wheels.

# Strategy

We are given information about the linear velocities of the motorcycle. Thus, we can find its linear acceleration  .   
Then, the expression  can be used to find the angular acceleration.

# Solution

The linear acceleration is



We also know the radius of the wheels. Entering the values for  and  into  , we get

# Discussion

Units of radians are dimensionless and appear in any relationship between angular and linear quantities.

So far, we have defined three rotational quantities—  ,  , and  . These quantities are analogous to the translational quantities  , and . Table 10.1 displays rotational quantities, the analogous translational quantities, and the relationships between them.

TABLE 10.1 Rotational and Translational Quantities   

<table><tr><td rowspan=1 colspan=3>Rotational  Translational  Relationship</td></tr><tr><td rowspan=1 colspan=1>θ</td><td rowspan=1 colspan=1>x</td><td rowspan=1 colspan=1>θ= \fracx}\alpha$ and its most common units are . The direction of angular acceleration along a fixed axis is denoted by  or a – sign, just as the direction of linear acceleration in one dimension is denoted by  or a – sign. For example, consider a gymnast doing a forward flip. Her angular momentum would be parallel to the mat and to her left. The magnitude of her angular acceleration would be proportional to her angular velocity (spin rate) and her moment of inertia about her spin axis.

# Ladybug Revolution

Join the ladybug in an exploration of rotational motion. Rotate the merry-go-round to change its angle, or choose a constant angular velocity or angular acceleration. Explore how circular motion relates to the bug's x,y position, velocity, and acceleration using vectors or graphs.

Click to view content (https://openstax.org/l/28ladybugrevolutionrotation).# 10.2 Kinematics of Rotational Motion

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Observe the kinematics of rotational motion.   
Derive rotational kinematic equations.   
Evaluate problem solving strategies for rotational kinematics.

Just by using our intuition, we can begin to see how rotational quantities like  ,  , and  are related to one another. For example, if a motorcycle wheel has a large angular acceleration for a fairly long time, it ends up spinning rapidly and rotates through many revolutions. In more technical terms, if the wheel’s angular acceleration  is large for a long period of time , then the final angular velocity  and angle of rotation  are large. The wheel’s rotational motion is exactly analogous to the fact that the motorcycle’s large translational acceleration produces a large final velocity, and the distance traveled will also be large.

Kinematics is the description of motion. The kinematics of rotational motion describes the relationships among rotation angle, angular velocity, angular acceleration, and time. Let us start by finding an equation relating  , and . To determine this equation, we recall a familiar kinematic equation for translational, or straight-line, motion:



Note that in rotational motion  , and we shall use the symbol  for tangential or linear acceleration from now on. As in linear kinematics, we assume  is constant, which means that angular acceleration  is also a constant, because  . Now, let us substitute  and  into the linear equation above:



The radius  cancels in the equation, yielding



where  is the initial angular velocity. This last equation is a kinematic relationship among  , and  —that is, it describes their relationship without reference to forces or masses that may affect rotation. It is also precisely analogous in form to its translational counterpart.

# Making Connections

Kinematics for rotational motion is completely analogous to translational kinematics, first presented in OneDimensional Kinematics. Kinematics is concerned with the description of motion without regard to force or mass. We will find that translational kinematic quantities, such as displacement, velocity, and acceleration have direct analogs in rotational motion.

Starting with the four kinematic equations we developed in One-Dimensional Kinematics, we can derive the following four rotational kinematic equations (presented together with their translational counterparts):

TABLE 10.2 Rotational Kinematic Equations   

<table><tr><td rowspan=1 colspan=3>Rotational        Translational</td></tr><tr><td rowspan=1 colspan=1>θ = t</td><td rowspan=1 colspan=1>x = Ut</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ω = ω0 + αt</td><td rowspan=1 colspan=1>U = U0 + at</td><td rowspan=1 colspan=1>(constant α, a)</td></tr><tr><td rowspan=1 colspan=1>1θ = ω0 +-α122</td><td rowspan=1 colspan=1>1at2 =  +2</td><td rowspan=1 colspan=1>(constant α, a)</td></tr><tr><td rowspan=1 colspan=1>2 =0{ +2αθ</td><td rowspan=1 colspan=1>v2 = 02 + 2x</td><td rowspan=1 colspan=1>(constant α, a)</td></tr></table>In these equations, the subscript 0 denotes initial values  , and  are initial values), and the average angular velocity  and average velocity  are defined as follows:



The equations given above in Table 10.2 can be used to solve any rotational or translational kinematics problem in which  and  are constant.

# Problem-Solving Strategy for Rotational Kinematics

1. Examine the situation to determine that rotational kinematics (rotational motion) is involved. Rotation mu be involved, but without the need to consider forces or masses that affect the motion.   
2. Identify exactly what needs to be determined in the problem (identify the unknowns). A sketch of the situation is useful.   
3. Make a list of what is given or can be inferred from the problem as stated (identify the knowns).   
4. Solve the appropriate equation or equations for the quantity to be determined (the unknown). It can be useful to think in terms of a translational analog because by now you are familiar with such motion.   
5. Substitute the known values along with their units into the appropriate equation, and obtain numerical solutions complete with units. Be sure to use units of radians for angles.   
6. Check your answer to see if it is reasonable: Does your answer make sense?

# EXAMPLE 10.3

# Calculating the Acceleration of a Fishing Reel

A deep-sea fisherman hooks a big fish that swims away from the boat pulling the fishing line from his fishing reel. The whole system is initially at rest and the fishing line unwinds from the reel at a radius of  from its axis of rotation. The reel is given an angular acceleration of  for  as seen in Figure 10.7.

(a) What is the final angular velocity of the reel? (b) At what speed is fishing line leaving the reel after 2.00 s elapses? (c) How many revolutions does the reel make? (d) How many meters of fishing line come off the reel in this time?

# Strategy

In each part of this example, the strategy is the same as it was for solving problems in linear kinematics. In particular, known values are identified and a relationship is then sought that can be used to solve for the unknown.

# Solution for (a)

Here  and  are given and  needs to be determined. The most straightforward equation to use is  because the unknown is already on one side and all other terms are known. That equation states that



We are also given that  (it starts from rest), so that



# Solution for (b)

Now that  is known, the speed  can most easily be found using the relationship



where the radius  of the reel is given to be  ; thus,

Note again that radians must always be used in any calculation relating linear and angular quantities. Also, because radians are dimensionless, we have  .

# Solution for (c)

Here, we are asked to find the number of revolutions. Because  , we can find the number of revolutions by finding  in radians. We are given  and  , and we know  is zero, so that  can be obtained using  .



Converting radians to revolutions gives



# Solution for (d)

The number of meters of fishing line is  , which can be obtained through its relationship with  :



# Discussion

This example illustrates that relationships among rotational quantities are highly analogous to those among linear quantities. We also see in this example how linear and rotational quantities are connected. The answers to the questions are realistic. After unwinding for two seconds, the reel is found to spin at  , which is 2100 rpm. (No wonder reels sometimes make high-pitched sounds.) The amount of fishing line played out is  , about right for when the big fish bites.

  
FIGURE 10.7 Fishing line coming off a rotating reel moves linearly. Example 10.3 and Example 10.4 consider relationships between rotational and linear quantities associated with a fishing reel.

# EXAMPLE 10.4

# Calculating the Duration When the Fishing Reel Slows Down and Stops

Now let us consider what happens if the fisherman applies a brake to the spinning reel, achieving an angular acceleration of  . How long does it take the reel to come to a stop?

# Strategy

We are asked to find the time  for the reel to come to a stop. The initial and final conditions are different from those in the previous problem, which involved the same fishing reel. Now we see that the initial angular velocity is  and the final angular velocity  is zero. The angular acceleration is given to be  .Examining the available equations, we see all quantities but t are known in  making it easiest to use this equation.

# Solution

The equation states



We solve the equation algebraically for  , and then substitute the known values as usual, yielding



# Discussion

Note that care must be taken with the signs that indicate the directions of various quantities. Also, note that the time to stop the reel is fairly small because the acceleration is rather large. Fishing lines sometimes snap because of the accelerations involved, and fishermen often let the fish swim for a while before applying brakes on the reel. A tired fish will be slower, requiring a smaller acceleration.

# EXAMPLE 10.5

# Calculating the Slow Acceleration of Trains and Their Wheels

Large freight trains accelerate very slowly. Suppose one such train accelerates from rest, giving its  -radius wheels an angular acceleration of  . After the wheels have made 200 revolutions (assume no slippage): (a) How far has the train moved down the track? (b) What are the final angular velocity of the wheels and the linear velocity of the train?

# Strategy

In part (a), we are asked to find  , and in (b) we are asked to find  and  . We are given the number of revolutions  , the radius of the wheels  , and the angular acceleration  .

# Solution for (a)

The distance  is very easily found from the relationship between distance and rotation angle:



Solving this equation for  yields



Before using this equation, we must convert the number of revolutions into radians, because we are dealing with a relationship between linear and rotational quantities:



Now we can substitute the known values into  to find the distance the train moved down the track:



# Solution for (b)

We cannot use any equation that incorporates  to find  , because the equation would have at least two unknown values. The equation  will work, because we know the values for all variables except  :



Taking the square root of this equation and entering the known values gives

We can find the linear velocity of the train,  , through its relationship to  :



# Discussion

The distance traveled is fairly large and the final velocity is fairly slow (just under  ).

There is translational motion even for something spinning in place, as the following example illustrates. Figure 10.8 shows a fly on the edge of a rotating microwave oven plate. The example below calculates the total distance it travels.

  
FIGURE 10.8 The image shows a microwave plate. The fly makes revolutions while the food is heated (along with the fly).

# EXAMPLE 10.6

# Calculating the Distance Traveled by a Fly on the Edge of a Microwave Oven Plate

A person decides to use a microwave oven to reheat some lunch. In the process, a fly accidentally flies into the microwave and lands on the outer edge of the rotating plate and remains there. If the plate has a radius of  and rotates at 6.0 rpm, calculate the total distance traveled by the fly during a 2.0-min cooking period. (Ignore the start-up and slow-down times.)

# Strategy

First, find the total number of revolutions  , and then the linear distance  traveled.  can be used to find  because  is given to be 6.0 rpm.

# Solution

Entering known values into  gives



As always, it is necessary to convert revolutions to radians before calculating a linear quantity like  from an angular quantity like  :



Now, using the relationship between  and  , we can determine the distance traveled:

# Discussion

Quite a trip (if it survives)! Note that this distance is the total distance traveled by the fly. Displacement is actually zero for complete revolutions because they bring the fly back to its original position. The distinction between total distance traveled and displacement was first noted in One-Dimensional Kinematics.

# CHECK YOUR UNDERSTANDING

Rotational kinematics has many useful relationships, often expressed in equation form. Are these relationships laws of physics or are they simply descriptive? (Hint: the same question applies to linear kinematics.)

# Solution

Rotational kinematics (just like linear kinematics) is descriptive and does not represent laws of nature. With kinematics, we can describe many things to great precision but kinematics does not consider causes. For example, a large angular acceleration describes a very rapid change in angular velocity without any consideration of its cause.

# 10.3 Dynamics of Rotational Motion: Rotational Inertia

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Understand the relationship between force, mass and acceleration.   
Study the turning effect of force.   
Study the analogy between force and torque, mass and moment of inertia, and linear acceleration and angular acceleration.

If you have ever spun a bike wheel or pushed a merry-go-round, you know that force is needed to change angular velocity as seen in Figure 10.9. In fact, your intuition is reliable in predicting many of the factors that are involved. For example, we know that a door opens slowly if we push too close to its hinges. Furthermore, we know that the more massive the door, the more slowly it opens. The first example implies that the farther the force is applied from the pivot, the greater the angular acceleration; another implication is that angular acceleration is inversely proportional to mass. These relationships should seem very similar to the familiar relationships among force, mass, and acceleration embodied in Newton’s second law of motion. There are, in fact, precise rotational analogs to both force and mass.

  
FIGURE 10.9 Force is required to spin the bike wheel. The greater the force, the greater the angular acceleration produced. The more massive the wheel, the smaller the angular acceleration. If you push on a spoke closer to the axle, the angular acceleration will be smaller.

To develop the precise relationship among force, mass, radius, and angular acceleration, consider what happens if we exert a force  on a point mass  that is at a distance  from a pivot point, as shown in Figure 10.10. Because the force is perpendicular to  , an acceleration  is obtained in the direction of  . We can rearrange this equation such that  and then look for ways to relate this expression to expressions for rotational quantities. We note that  , and we substitute this expression into  , yielding



Recall that torque is the turning effectiveness of a force. In this case, because  is perpendicular to  , torque is simply  . So, if we multiply both sides of the equation above by  , we get torque on the left-hand side. That is,



This last equation is the rotational analog of Newton’s second law (  ), where torque is analogous to force, angular acceleration is analogous to translational acceleration, and  is analogous to mass (or inertia). The quantity  is called the rotational inertia or moment of inertia of a point mass  a distance  from the center of rotation.

  
FIGURE 10.10 An object is supported by a horizontal frictionless table and is attached to a pivot point by a cord that supplies centripetal force. A force  is applied to the object perpendicular to the radius  causing it to accelerate about the pivot point. The force is kept perpendicular to  .

# Making Connections: Rotational Motion Dynamics

Dynamics for rotational motion is completely analogous to linear or translational dynamics. Dynamics is concerned with force and mass and their effects on motion. For rotational motion, we will find direct analogs to force and mass that behave just as we would expect from our earlier experiences.

# Rotational Inertia and Moment of Inertia

Before we can consider the rotation of anything other than a point mass like the one in Figure 10.10, we must extend the idea of rotational inertia to all types of objects. To expand our concept of rotational inertia, we define the moment of inertia  of an object to be the sum of  for all the point masses of which it is composed. That is,  . Here  is analogous to  in translational motion. Because of the distance  , the moment of inertia for any object depends on the chosen axis. Actually, calculating  is beyond the scope of this text except for one simple case—that of a hoop, which has all its mass at the same distance from its axis. A hoop’s moment of inertia around its axis is therefore  , where  is its total mass and  its radius. (We use  and  for an entire object to distinguish them from  and  for point masses.) In all other cases, we must consult Figure 10.11 (note that the table is piece of artwork that has shapes as well as formulae) for formulas for  that have been derived from integration over the continuous body. Note that  has units of mass multiplied by distance squared  , as we might expect from its definition.

The general relationship among torque, moment of inertia, and angular acceleration is



or



where net  is the total torque from all forces relative to a chosen axis. For simplicity, we will only consider torques exerted by forces in the plane of the rotation. Such torques are either positive or negative and add like ordinary numbers. The relationship in  :  is the rotational analog to Newton’s second law and is very generally applicable. This equation is actually valid for any torque, applied to any object, relative to any axis.

As we might expect, the larger the torque is, the larger the angular acceleration is. For example, the harder a childpushes on a merry-go-round, the faster it accelerates. Furthermore, the more massive a merry-go-round, the slower it accelerates for the same torque. The basic relationship between moment of inertia and angular acceleration is that the larger the moment of inertia, the smaller is the angular acceleration. But there is an additional twist. The moment of inertia depends not only on the mass of an object, but also on its distribution of mass relative to the axis around which it rotates. For example, it will be much easier to accelerate a merry-go-round full of children if they stand close to its axis than if they all stand at the outer edge. The mass is the same in both cases, but the moment of inertia is much larger when the children are at the edge.

# Take-Home Experiment

Cut out a circle that has about a 10 cm radius from stiff cardboard. Near the edge of the circle, write numbers 1 to 12 like hours on a clock face. Position the circle so that it can rotate freely about a horizontal axis through its center, like a wheel. (You could loosely nail the circle to a wall.) Hold the circle stationary and with the number 12 positioned at the top, attach a lump of blue putty (sticky material used for fixing posters to walls) at the number 3. How large does the lump need to be to just rotate the circle? Describe how you can change the moment of inertia of the circle. How does this change affect the amount of blue putty needed at the number 3 to just rotate the circle? Change the circle’s moment of inertia and then try rotating the circle by using different amounts of blue putty. Repeat this process several times.

# Problem-Solving Strategy for Rotational Dynamics

1. Examine the situation to determine that torque and mass are involved in the rotation. Draw a careful sketch of the situation.   
2. Determine the system of interest.   
3. Draw a free body diagram. That is, draw and label all external forces acting on the system of interest.   
4. Apply   , the rotational equivalent of Newton’s second law, to solve the problem. Care must be taken to use the correct moment of inertia and to consider the torque about the point of rotation.   
5. As always check the solution to see if it is reasonable.

# Making Connections

In statics, the net torque is zero, and there is no angular acceleration. In rotational motion, net torque is the cause of angular acceleration, exactly as in Newton’s second law of motion for rotation.  
FIGURE 10.11 Some rotational inertias.

# EXAMPLE 10.7

# Calculating the Effect of Mass Distribution on a Merry-Go-Round

Consider the father pushing a playground merry-go-round in Figure 10.12. He exerts a force of  at the edge of the  merry-go-round, which has a  radius. Calculate the angular acceleration produced (a) when no one is on the merry-go-round and (b) when an  child sits  away from the center. Consider the merrygo-round itself to be a uniform disk with negligible retarding friction.  
FIGURE 10.12 A father pushes a playground merry-go-round at its edge and perpendicular to its radius to achieve maximum torque.

# Strategy

Angular acceleration is given directly by the expression :



To solve for  , we must first calculate the torque  (which is the same in both cases) and moment of inertia  (which is greater in the second case). To find the torque, we note that the applied force is perpendicular to the radius and friction is negligible, so that



# Solution for (a)

The moment of inertia of a solid disk about this axis is given in Figure 10.11 to be



where  and  , so that



Now, after we substitute the known values, we find the angular acceleration to be



# Solution for (b)

We expect the angular acceleration for the system to be less in this part, because the moment of inertia is greater when the child is on the merry-go-round. To find the total moment of inertia  , we first find the child’s moment of inertia  by considering the child to be equivalent to a point mass at a distance of  from the axis. Then,



The total moment of inertia is the sum of moments of inertia of the merry-go-round and the child (about the same axis). To justify this sum to yourself, examine the definition of  :



Substituting known values into the equation for  gives



# Discussion

The angular acceleration is less when the child is on the merry-go-round than when the merry-go-round is empty, as expected. The angular accelerations found are quite large, partly due to the fact that friction was considered to benegligible. If, for example, the father kept pushing perpendicularly for 2.00 s, he would give the merry-go-round an angular velocity of  when it is empty but only 8.89 rad/s when the child is on it. In terms of revolutions per second, these angular velocities are 2.12 rev/s and 1.41 rev/s, respectively. The father would end up running at about  in the first case. Summer Olympics, here he comes! Confirmation of these numbers is left as an exercise for the reader.

# CHECK YOUR UNDERSTANDING

Torque is the analog of force and moment of inertia is the analog of mass. Force and mass are physical quantities that depend on only one factor. For example, mass is related solely to the numbers of atoms of various types in an object. Are torque and moment of inertia similarly simple?

# Solution

No. Torque depends on three factors: force magnitude, force direction, and point of application. Moment of inertia depends on both mass and its distribution relative to the axis of rotation. So, while the analogies are precise, these rotational quantities depend on more factors.

# 10.4 Rotational Kinetic Energy: Work and Energy Revisited

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Derive the equation for rotational work.   
Calculate rotational kinetic energy.   
Demonstrate the Law of Conservation of Energy.

In this module, we will learn about work and energy associated with rotational motion. Figure 10.13 shows a worker using an electric grindstone propelled by a motor. Sparks are flying, and noise and vibration are created as layers of steel are pared from the pole. The stone continues to turn even after the motor is turned off, but it is eventually brought to a stop by friction. Clearly, the motor had to work to get the stone spinning. This work went into heat, light, sound, vibration, and considerable rotational kinetic energy.

  
FIGURE 10.13 The motor works in spinning the grindstone, giving it rotational kinetic energy. That energy is then converted to heat, light, sound, and vibration. (credit: U.S. Navy photo by Mass Communication Specialist Seaman Zachary David Bell)

Work must be done to rotate objects such as grindstones or merry-go-rounds. Work was defined in Uniform Circular Motion and Gravitation for translational motion, and we can build on that knowledge when considering work done in rotational motion. The simplest rotational situation is one in which the net force is exerted perpendicular to the radius of a disk (as shown in Figure 10.14) and remains perpendicular as the disk starts to rotate. The force is parallel to the displacement, and so the net work done is the product of the force times the arc length traveled:

To get torque and other rotational quantities into the equation, we multiply and divide the right-hand side of the equation by  , and gather terms:



We recognize that  net  net  and  , so thatThis equation is the expression for rotational work. It is very similar to the familiar definition of translational work as force multiplied by distance. Here, torque is analogous to force, and angle is analogous to distance. The equation net  is valid in general, even though it was derived for a special case.

To get an expression for rotational kinetic energy, we must again perform some algebraic manipulations. The first step is to note that  , so that

  
FIGURE 10.14 The net force on this disk is kept perpendicular to its radius as the force causes the disk to rotate. The net work done is thus (net  . The net work goes into rotational kinetic energy.

# Making Connections

Work and energy in rotational motion are completely analogous to work and energy in translational motion, first presented in Uniform Circular Motion and Gravitation.

Now, we solve one of the rotational kinematics equations for  . We start with the equation



Next, we solve for :



Substituting this into the equation for net  and gathering terms yields



This equation is the work-energy theorem for rotational motion only. As you may recall, net work changes the kinetic energy of a system. Through an analogy with translational motion, we define the term  to be rotational kinetic energy  for an object with a moment of inertia  and an angular velocity  :



The expression for rotational kinetic energy is exactly analogous to translational kinetic energy, with  being analogous to  and  to  . Rotational kinetic energy has important effects. Flywheels, for example, can be used to store large amounts of rotational kinetic energy in a vehicle, as seen in Figure 10.15.  
FIGURE 10.15 Experimental vehicles, such as this bus, have been constructed in which rotational kinetic energy is stored in a large flywheel. When the bus goes down a hill, its transmission converts its gravitational potential energy into  . It can also convert translational kinetic energy, when the bus stops, into  . The flywheel’s energy can then be used to accelerate, to  up another hill, or to keep the bus from slowing down due to friction.

# EXAMPLE 10.8

# Calculating the Work and Energy for Spinning a Grindstone

Consider a person who spins a large grindstone by placing her hand on its edge and exerting a force through part of a revolution as shown in Figure 10.16. In this example, we verify that the work done by the torque she exerts equals the change in rotational energy. (a) How much work is done if she exerts a force of  through a rotation of  The force is kept perpendicular to the grindstone’s  radius at the point of application, and the effects of friction are negligible. (b) What is the final angular velocity if the grindstone has a mass of  (c) What is the final rotational kinetic energy? (It should equal the work.)

# Strategy

To find the work, we can use the equation  . We have enough information to calculate the torque and are given the rotation angle. In the second part, we can find the final angular velocity using one of the kinematic relationships. In the last part, we can calculate the rotational kinetic energy from its expression in  .

# Solution for (a)

The net work is expressed in the equation



where net  is the applied force multiplied by the radius  because there is no retarding friction, and the force is perpendicular to  . The angle  is given. Substituting the given values in the equation above yields



Noting that  ,

  
FIGURE 10.16 A large grindstone is given a spin by a person grasping its outer edge.# Solution for (b)

To find  from the given information requires more than one step. We start with the kinematic relationship in the equation



Note that  because we start from rest. Taking the square root of the resulting equation gives



Now we need to find  . One possibility is



where the torque is



The formula for the moment of inertia for a disk is found in Figure 10.11:



Substituting the values of torque and moment of inertia into the expression for  , we obtain



Now, substitute this value and the given value for  into the above expression for  :



# Solution for (c)

The final rotational kinetic energy is



Both  and  were found above. Thus,



# Discussion

The final rotational kinetic energy equals the work done by the torque, which confirms that the work done went into rotational kinetic energy. We could, in fact, have used an expression for energy instead of a kinematic relation to solve part (b). We will do this in later examples.

Helicopter pilots are quite familiar with rotational kinetic energy. They know, for example, that a point of no return will be reached if they allow their blades to slow below a critical angular velocity during flight. The blades lose lift, and it is impossible to immediately get the blades spinning fast enough to regain it. Rotational kinetic energy must be supplied to the blades to get them to rotate faster, and enough energy cannot be supplied in time to avoid a crash. Because of weight limitations, helicopter engines are too small to supply both the energy needed for lift and to replenish the rotational kinetic energy of the blades once they have slowed down. The rotational kinetic energy is put into them before takeoff and must not be allowed to drop below this crucial level. One possible way to avoid a crash is to use the gravitational potential energy of the helicopter to replenish the rotational kinetic energy of the blades by losing altitude and aligning the blades so that the helicopter is spun up in the descent. Of course, if the helicopter’s altitude is too low, then there is insufficient time for the blade to regain lift before reaching the ground.# Problem-Solving Strategy for Rotational Energy

1. Determine that energy or work is involved in the rotation.   
2. Determine the system of interest. A sketch usually helps.   
3. Analyze the situation to determine the types of work and energy involved.   
4. For closed systems, mechanical energy is conserved. That is,  Note that  and  may each include translational and rotational contributions.   
5. For open systems, mechanical energy may not be conserved, and other forms of energy (referred to previously as  ), such as heat transfer, may enter or leave the system. Determine what they are, and calculate them as necessary.   
6. Eliminate terms wherever possible to simplify the algebra.   
7. Checkthe answer to see if it is reasonable.

# EXAMPLE 10.9

# Calculating Helicopter Energies

A typical small rescue helicopter, similar to the one in Figure 10.17, has four blades, each is  long and has a mass of  . The blades can be approximated as thin rods that rotate about one end of an axis perpendicular to their length. The helicopter has a total loaded mass of  . (a) Calculate the rotational kinetic energy in the blades when they rotate at 300 rpm. (b) Calculate the translational kinetic energy of the helicopter when it flies at  , and compare it with the rotational energy in the blades. (c) To what height could the helicopter be raised if all of the rotational kinetic energy could be used to lift it?

# Strategy

Rotational and translational kinetic energies can be calculated from their definitions. The last part of the problem relates to the idea that energy can change form, in this case from rotational kinetic energy to gravitational potential energy.

# Solution for (a)

The rotational kinetic energy is



We must convert the angular velocity to radians per second and calculate the moment of inertia before we can find  . The angular velocity  is



The moment of inertia of one blade will be that of a thin rod rotated about its end, found in Figure 10.11. The total  is four times this moment of inertia, because there are four blades. Thus,



Entering  and  into the expression for rotational kinetic energy gives



# Solution for (b)

Translational kinetic energy was defined in Uniform Circular Motion and Gravitation. Entering the given values of mass and velocity, we obtain

To compare kinetic energies, we take the ratio of translational kinetic energy to rotational kinetic energy. This ratio is



# Solution for (c)

At the maximum height, all rotational kinetic energy will have been converted to gravitational energy. To find this height, we equate those two energies:



or



We now solve for  and substitute known values into the resulting equation



# Discussion

The ratio of translational energy to rotational kinetic energy is only 0.380. This ratio tells us that most of the kinetic energy of the helicopter is in its spinning blades—something you probably would not suspect. The  height to which the helicopter could be raised with the rotational kinetic energy is also impressive, again emphasizing the amount of rotational kinetic energy in the blades.

  
FIGURE 10.17 The first image shows how helicopters store large amounts of rotational kinetic energy in their blades. This energy must be put into the blades before takeoff and maintained until the end of the flight. The engines do not have enough power to simultaneously provide lift and put significant rotational energy into the blades. The second image shows a helicopter from the Auckland Westpac Rescue Helicopter Service. Over 50,000 lives have been saved since its operations beginning in 1973. Here, a water rescue operation is shown. (credit: 111 Emergency, Flickr)# Making Connections

Conservation of energy includes rotational motion, because rotational kinetic energy is another form of .   
Uniform Circular Motion and Gravitation has a detailed treatment of conservation of energy.

# How Thick Is the Soup? Or Why Don’t All Objects Roll Downhill at the Same Rate?

One of the quality controls in a tomato soup factory consists of rolling filled cans down a ramp. If they roll too fast, the soup is too thin. Why should cans of identical size and mass roll down an incline at different rates? And why should the thickest soup roll the slowest?

The easiest way to answer these questions is to consider energy. Suppose each can starts down the ramp from rest. Each can starting from rest means each starts with the same gravitational potential energy  , which is converted entirely to , provided each rolls without slipping. , however, can take the form of  or  , and total is the sum of the two. If a can rolls down a ramp, it puts part of its energy into rotation, leaving less for translation. Thus, the can goes slower than it would if it slid down. Furthermore, the thin soup does not rotate, whereas the thick soup does, because it sticks to the can. The thick soup thus puts more of the can’s original gravitational potential energy into rotation than the thin soup, and the can rolls more slowly, as seen in Figure 10.18.

  
FIGURE 10.18 Three cans of soup with identical masses race down an incline. The first can has a low friction coating and does not roll but just slides down the incline. It wins because it converts its entire PE into translational KE. The second and third cans both roll down the incline without slipping. The second can contains thin soup and comes in second because part of its initial PE goes into rotating the can (but not the thin soup). The third can contains thick soup. It comes in third because the soup rotates along with the can, taking even more of the initial PE for rotational KE, leaving less for translational KE.

Assuming no losses due to friction, there is only one force doing work—gravity. Therefore the total work done is the change in kinetic energy. As the cans start moving, the potential energy is changing into kinetic energy. Conservation of energy gives



More specifically,



or



So, the initial is divided between translational kinetic energy and rotational kinetic energy; and the greater  is, the less energy goes into translation. If the can slides down without friction, then  and all the energy goes into translation; thus, the can goes faster.

# Take-Home Experiment

Locate several cans each containing different types of food. First, predict which can will win the race down an inclined plane and explain why. See if your prediction is correct. You could also do this experiment by collecting several empty cylindrical containers of the same size and filling them with different materials such as wet or dry sand.# EXAMPLE 10.10

# Calculating the Speed of a Cylinder Rolling Down an Incline

Calculate the final speed of a solid cylinder that rolls down a  -high incline. The cylinder starts from rest, has a mass of  , and has a radius of  .

# Strategy

We can solve for the final velocity using conservation of energy, but we must first express rotational quantities in terms of translational quantities to end up with  as the only unknown.

# Solution

Conservation of energy for this situation is written as described above:



Before we can solve for  , we must get an expression for  from Figure 10.11. Because  and  are related (note here that the cylinder is rolling without slipping), we must also substitute the relationship  into the expression. These substitutions yield



Interestingly, the cylinder’s radius  and mass  cancel, yielding



Solving algebraically, the equation for the final velocity  gives



Substituting known values into the resulting expression yields



# Discussion

Because and cancel, the result i s valid for any solid cylinder, implying that all solid cylinders will roll down an incline at the same rate independent of their masses and sizes. (Rolling cylinders down inclines is what Galileo actually did to show that objects fall at the same rate independent of mass.) Note that if the cylinder slid without friction down the incline without rolling, then the entire gravitational potential energy would go into translational kinetic energy. Thus,  and  , which is  greater than  . That is, the cylinder would go faster at the bottom.

# CHECK YOUR UNDERSTANDING

Analogy of Rotational and Translational Kinetic Energy Is rotational kinetic energy completely analogous to translational kinetic energy? What, if any, are their differences? Give an example of each type of kinetic energy.

# Solution

Yes, rotational and translational kinetic energy are exact analogs. They both are the energy of motion involved with the coordinated (non-random) movement of mass relative to some reference frame. The only difference between rotational and translational kinetic energy is that translational is straight line motion while rotational is not. Anexample of both kinetic and translational kinetic energy is found in a bike tire while being ridden down a bike path. The rotational motion of the tire means it has rotational kinetic energy while the movement of the bike along the path means the tire also has translational kinetic energy. If you were to lift the front wheel of the bike and spin it while the bike is stationary, then the wheel would have only rotational kinetic energy relative to the Earth.

# 10.5 Angular Momentum and Its Conservation

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Understand the analogy between angular momentum and linear momentum.   
Observe the relationship between torque and angular momentum.   
Apply the law of conservation of angular momentum.

Why does Earth keep on spinning? What started it spinning to begin with? And how does an ice skater manage to spin faster and faster simply by pulling her arms in? Why does she not have to exert a torque to spin faster? Questions like these have answers based in angular momentum, the rotational analog to linear momentum.

By now the pattern is clear—every rotational phenomenon has a direct translational analog. It seems quite reasonable, then, to define angular momentum  as



This equation is an analog to the definition of linear momentum as  . Units for linear momentum are  while units for angular momentum are  . As we would expect, an object that has a large moment of inertia  , such as Earth, has a very large angular momentum. An object that has a large angular velocity  , such as a centrifuge, also has a rather large angular momentum.

# Making Connections

Angular momentum is completely analogous to linear momentum, first presented in Uniform Circular Motion and Gravitation. It has the same implications in terms of carrying rotation forward, and it is conserved when the net external torque is zero. Angular momentum, like linear momentum, is also a property of the atoms and subatomic particles.

# EXAMPLE 10.11

# Calculating Angular Momentum of the Earth Strategy

No information is given in the statement of the problem; so we must look up pertinent data before we can calculate  . First, according to Figure 10.11, the formula for the moment of inertia of a sphere is



so that



Earth’s mass  is  and its radius  is  . The Earth’s angular velocity  is, of course, exactly one revolution per day, but we must covert  to radians per second to do the calculation in SI units.

# Solution

Substituting known information into the expression for  and converting  to radians per second gives

Substituting  rad for rev and  for 1 day gives



# Discussion

This number is large, demonstrating that Earth, as expected, has a tremendous angular momentum. The answer is approximate, because we have assumed a constant density for Earth in order to estimate its moment of inertia.

When you push a merry-go-round, spin a bike wheel, or open a door, you exert a torque. If the torque you exert is greater than opposing torques, then the rotation accelerates, and angular momentum increases. The greater the net torque, the more rapid the increase in  . The relationship between torque and angular momentum is



This expression is exactly analogous to the relationship between force and linear momentum,  . The equation  is very fundamental and broadly applicable. It is, in fact, the rotational form of Newton’s second law.

# EXAMPLE 10.12

# Calculating the Torque Putting Angular Momentum Into a Rotating Food Tray

Figure 10.19 shows a rotating food tray, often called a lazy Susan, being turned by a person in quest of sustenance. Suppose the person exerts a  force perpendicular to the lazy Susan’s  radius for 0.150 s. (a) What is the final angular momentum of the lazy Susan if it starts from rest, assuming friction is negligible? (b) What is the final angular velocity of the lazy Susan, given that its mass is  and assuming its moment of inertia is that of a disk?

  
FIGURE 10.19 A partygoer exerts a torque on a lazy Susan to make it rotate. The equation  gives the relationship between torque and the angular momentum produced.

# Strategy

We can find the angular momentum by solving  for  , and using the given information to calculate the torque. The final angular momentum equals the change in angular momentum, because the lazy Susan starts from rest. That is,  . To find the final velocity, we must calculate  from the definition of  in  .

# Solution for (a)

Solving  for gives

Because the force is perpendicular to  , we see that  , so that



# Solution for (b)

The final angular velocity can be calculated from the definition of angular momentum,



Solving for  and substituting the formula for the moment of inertia of a disk into the resulting equation gives



And substituting known values into the preceding equation yields



# Discussion

Note that the imparted angular momentum does not depend on any property of the object but only on torque and time. The final angular velocity is equivalent to one revolution in 8.71 s (determination of the time period is left as an exercise for the reader), which is about right for a lazy Susan.

# EXAMPLE 10.13

# Calculating the Torque in a Kick

The person whose leg is shown in Figure 10.20 kicks his leg by exerting a 2000-N force with his upper leg muscle. The effective perpendicular lever arm is  . Given the moment of inertia of the lower leg is  , (a) find the angular acceleration of the leg. (b) Neglecting the gravitational force, what is the rotational kinetic energy of the leg after it has rotated through  (1.00 rad)?

  
FIGURE 10.20 The muscle in the upper leg gives the lower leg an angular acceleration and imparts rotational kinetic energy to it by exerting a torque about the knee. is a vector that is perpendicular to  . This example examines the situation.

# Strategy

The angular acceleration can be found using the rotational analog to Newton’s second law, or  . The moment of inertia  is given and the torque can be found easily from the given force and perpendicular lever arm. Once the angular acceleration  is known, the final angular velocity and rotational kinetic energy can be calculated.

# Solution to (a)

From the rotational analog to Newton’s second law, the angular acceleration  is

Because the force and the perpendicular lever arm are given and the leg is vertical so that its weight does not create a torque, the net torque is thus



Substituting this value for the torque and the given value for the moment of inertia into the expression for  gives



# Solution to (b)

The final angular velocity can be calculated from the kinematic expression



or



because the initial angular velocity is zero. The kinetic energy of rotation is



so it is most convenient to use the value of  just found and the given value for the moment of inertia. The kinetic energy is then



# Discussion

These values are reasonable for a person kicking his leg starting from the position shown. The weight of the leg can be neglected in part (a) because it exerts no torque when the center of gravity of the lower leg is directly beneath the pivot in the knee. In part (b), the force exerted by the upper leg is so large that its torque is much greater than that created by the weight of the lower leg as it rotates. The rotational kinetic energy given to the lower leg is enough that it could give a ball a significant velocity by transferring some of this energy in a kick.

# Making Connections: Conservation Laws

Angular momentum, like energy and linear momentum, is conserved. This universally applicable law is another sign of underlying unity in physical laws. Angular momentum is conserved when net external torque is zero, just as linear momentum is conserved when the net external force is zero.

# Conservation of Angular Momentum

We can now understand why Earth keeps on spinning. As we saw in the previous example,  . This equation means that, to change angular momentum, a torque must act over some period of time. Because Earth has a large angular momentum, a large torque acting over a long time is needed to change its rate of spin. So what external torques are there? Tidal friction exerts torque that is slowing Earth’s rotation, but tens of millions of years must pass before the change is very significant. Recent research indicates the length of the day was  some 900 million years ago. Only the tides exert significant retarding torques on Earth, and so it will continue to spin, although ever more slowly, for many billions of years.What we have here is, in fact, another conservation law. If the net torque is zero, then angular momentum is constant or conserved. We can see this rigorously by considering  for the situation in which the net torque is zero. In that case,



implying that



If the change in angular momentum  is zero, then the angular momentum is constant; thus,



or



These expressions are the law of conservation of angular momentum. Conservation laws are as scarce as they are important.

An example of conservation of angular momentum is seen in Figure 10.21, in which an ice skater is executing a spin. The net torque on her is very close to zero, because there is relatively little friction between her skates and the ice and because the friction is exerted very close to the pivot point. (Both  and  are small, and so  is negligibly small.) Consequently, she can spin for quite some time. She can do something else, too. She can increase her rate of spin by pulling her arms and legs in. Why does pulling her arms and legs in increase her rate of spin? The answer is that her angular momentum is constant, so that



Expressing this equation in terms of the moment of inertia,



where the primed quantities refer to conditions after she has pulled in her arms and reduced her moment of inertia. Because  is smaller, the angular velocity  must increase to keep the angular momentum constant. The change can be dramatic, as the following example shows.

  
FIGURE 10.21 (a) An ice skater is spinning on the tip of her skate with her arms extended. Her angular momentum is conserved because the net torque on her is negligibly small. In the next image, her rate of spin increases greatly when she pulls in her arms, decreasing her moment of inertia. The work she does to pull in her arms results in an increase in rotational kinetic energy.

# EXAMPLE 10.14

# Calculating the Angular Momentum of a Spinning Skater

Suppose an ice skater, such as the one in Figure 10.21, is spinning at 0.800 rev/ s with her arms extended. She has a moment of inertia of  with her arms extended and of  with her arms close to her body. (These moments of inertia are based on reasonable assumptions about a  skater.) (a) What is her angular velocity in revolutions per second after she pulls in her arms? (b) What is her rotational kinetic energy before and after she does this?# Strategy

In the first part of the problem, we are looking for the skater’s angular velocity  after she has pulled in her arms. To find this quantity, we use the conservation of angular momentum and note that the moments of inertia and initial angular velocity are given. To find the initial and final kinetic energies, we use the definition of rotational kinetic energy given by



# Solution for (a)

Because torque is negligible (as discussed above), the conservation of angular momentum given in  is applicable. Thus,



or



Solving for  and substituting known values into the resulting equation gives



# Solution for (b)

Rotational kinetic energy is given by



The initial value is found by substituting known values into the equation and converting the angular velocity to 



The final rotational kinetic energy is



Substituting known values into this equation gives



# Discussion

In both parts, there is an impressive increase. First, the final angular velocity is large, although most world-class skaters can achieve spin rates about this great. Second, the final kinetic energy is much greater than the initial kinetic energy. The increase in rotational kinetic energy comes from work done by the skater in pulling in her arms. This work is internal work that depletes some of the skater’s food energy.

There are several other examples of objects that increase their rate of spin because something reduced their moment of inertia. Tornadoes are one example. Storm systems that create tornadoes are slowly rotating. When the radius of rotation narrows, even in a local region, angular velocity increases, sometimes to the furious level of a tornado. Earth is another example. Our planet was born from a huge cloud of gas and dust, the rotation of which came from turbulence in an even larger cloud. Gravitational forces caused the cloud to contract, and the rotation rate increased as a result. (See Figure 10.22.)  
FIGURE 10.22 The Solar System coalesced from a cloud of gas and dust that was originally rotating. The orbital motions and spins of the planets are in the same direction as the original spin and conserve the angular momentum of the parent cloud.

In case of human motion, one would not expect angular momentum to be conserved when a body interacts with the environment as its foot pushes off the ground. Astronauts floating in space aboard the International Space Station have no angular momentum relative to the inside of the ship if they are motionless. Their bodies will continue to have this zero value no matter how they twist about as long as they do not give themselves a push off the side of the vessel.

# CHECK YOUR UNDERSTANDING

Is angular momentum completely analogous to linear momentum? What, if any, are their differences?

# Solution

Yes, angular and linear momentums are completely analogous. While they are exact analogs they have different units and are not directly inter-convertible like forms of energy are.

# 10.6 Collisions of Extended Bodies in Two Dimensions

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Observe collisions of extended bodies in two dimensions. • Examine collision at the point of percussion.

Bowling pins are sent flying and spinning when hit by a bowling ball—angular momentum as well as linear momentum and energy have been imparted to the pins. (See Figure 10.23). Many collisions involve angular momentum. Cars, for example, may spin and collide on ice or a wet surface. Baseball pitchers throw curves by putting spin on the baseball. A tennis player can put a lot of top spin on the tennis ball which causes it to dive down onto the court once it crosses the net. We now take a brief look at what happens when objects that can rotate collide.

Consider the relatively simple collision shown in Figure 10.24, in which a disk strikes and adheres to an initially motionless stick nailed at one end to a frictionless surface. After the collision, the two rotate about the nail. There is an unbalanced external force on the system at the nail. This force exerts no torque because its lever arm  is zero. Angular momentum is therefore conserved in the collision. Kinetic energy is not conserved, because the collision is inelastic. It is possible that momentum is not conserved either because the force at the nail may have a component in the direction of the disk’s initial velocity. Let us examine a case of rotation in a collision in Example 10.15.  
FIGURE 10.23 The bowling ball causes the pins to fly, some of them spinning violently. (credit: Tinou Bao, Flickr)

  
FIGURE 10.24 (a) A disk slides toward a motionless stick on a frictionless surface. (b) The disk hits the stick at one end and adheres to it, and they rotate together, pivoting around the nail. Angular momentum is conserved for this inelastic collision because the surface is frictionless and the unbalanced external force at the nail exerts no torque.

# EXAMPLE 10.15

# Rotation in a Collision

Suppose the disk in Figure 10.24 has a mass of  and an initial velocity of  when it strikes the stick that is  long and  .

(a) What is the angular velocity of the two after the collision?

(b) What is the kinetic energy before and after the collision?

(c) What is the total linear momentum before and after the collision?

# Strategy for (a)

We can answer the first question using conservation of angular momentum as noted. Because angular momentum is  , we can solve for angular velocity.

# Solution for (a)

Conservation of angular momentum states



where primed quantities stand for conditions after the collision and both momenta are calculated relative to the pivot point. The initial angular momentum of the system of stick-disk is that of the disk just before it strikes the stick. That is,



where  is the moment of inertia of the disk and  is its angular velocity around the pivot point. Now,  (taking the disk to be approximately a point mass) and  , so that



After the collision,

It is  that we wish to find. Conservation of angular momentum gives



Rearranging the equation yields



where  is the moment of inertia of the stick and disk stuck together, which is the sum of their individual moments of inertia about the nail. Figure 10.11 gives the formula for a rod rotating around one end to be  . Thus,



Entering known values in this equation yields,



The value of  is now entered into the expression for  , which yields



# Strategy for (b)

The kinetic energy before the collision is the incoming disk’s translational kinetic energy, and after the collision, it is the rotational kinetic energy of the two stuck together.

# Solution for (b)

First, we calculate the translational kinetic energy by entering given values for the mass and speed of the incoming disk.



After the collision, the rotational kinetic energy can be found because we now know the final angular velocity and the final moment of inertia. Thus, entering the values into the rotational kinetic energy equation gives



# Strategy for (c)

The linear momentum before the collision is that of the disk. After the collision, it is the sum of the disk’s momentum and that of the center of mass of the stick.

# Solution of (c)

Before the collision, then, linear momentum is



After the collision, the disk and the stick’s center of mass move in the same direction. The total linear momentum is that of the disk moving at a new velocity  plus that of the stick’s center of mass,

which moves at half this speed because  . Thus,

Gathering similar terms in the equation yields,



so that



Substituting known values into the equation,



# Discussion

First note that the kinetic energy is less after the collision, as predicted, because the collision is inelastic. More surprising is that the momentum after the collision is actually greater than before the collision. This result can be understood if you consider how the nail affects the stick and vice versa. Apparently, the stick pushes backward on the nail when first struck by the disk. The nail’s reaction (consistent with Newton’s third law) is to push forward on the stick, imparting momentum to it in the same direction in which the disk was initially moving, thereby increasing the momentum of the system.

The above example has other implications. For example, what would happen if the disk hit very close to the nail? Obviously, a force would be exerted on the nail in the forward direction. So, when the stick is struck at the end farthest from the nail, a backward force is exerted on the nail, and when it is hit at the end nearest the nail, a forward force is exerted on the nail. Thus, striking it at a certain point in between produces no force on the nail. This intermediate point is known as the percussion point.

An analogous situation occurs in tennis as seen in Figure 10.25. If you hit a ball with the end of your racquet, the handle is pulled away from your hand. If you hit a ball much farther down, for example, on the shaft of the racquet, the handle is pushed into your palm. And if you hit the ball at the racquet’s percussion point (what some people call the “sweet spot”), then little or no force is exerted on your hand, and there is less vibration, reducing chances of a tennis elbow. The same effect occurs for a baseball bat.  
FIGURE 10.25 A disk hitting a stick is compared to a tennis ball being hit by a racquet. (a) When the ball strikes the racquet near the end, a backward force is exerted on the hand. (b) When the racquet is struck much farther down, a forward force is exerted on the hand. (c) When the racquet is struck at the percussion point, no force is delivered to the hand.

# CHECK YOUR UNDERSTANDING

Is rotational kinetic energy a vector? Justify your answer.

# Solution

No, energy is always scalar whether motion is involved or not. No form of energy has a direction in space and you can see that rotational kinetic energy does not depend on the direction of motion just as linear kinetic energy is independent of the direction of motion.# 10.7 Gyroscopic Effects: Vector Aspects of Angular Momentum

# LEARNING OBJECTIVES

By the end of this section, you will be able to:

Describe the right-hand rule to find the direction of angular velocity, momentum, and torque.   
Explain the gyroscopic effect.   
Study how Earth acts like a gigantic gyroscope.

Angular momentum is a vector and, therefore, has direction as well as magnitude. Torque affects both the direction and the magnitude of angular momentum. What is the direction of the angular momentum of a rotating object like the disk in Figure 10.26? The figure shows the right-hand rule used to find the direction of both angular momentum and angular velocity. Both and  are vectors—each has direction and magnitude. Both can be represented by arrows. The right-hand rule defines both to be perpendicular to the plane of rotation in the direction shown. Because angular momentum is related to angular velocity by  , the direction of  is the same as the direction of . Notice in the figure that both point along the axis of rotation.

  
FIGURE 10.26 Figure (a) shows a disk is rotating counterclockwise when viewed from above. Figure (b) shows the right-hand rule. The direction of angular velocity  size and angular momentum are defined to be the direction in which the thumb of your right hand points when you curl your fingers in the direction of the disk’s rotation as shown.

Now, recall that torque changes angular momentum as expressed by



This equation means that the direction of  is the same as the direction of the torque  that creates it. This result is illustrated in Figure 10.27, which shows the direction of torque and the angular momentum it creates.

Let us now consider a bicycle wheel with a couple of handles attached to it, as shown in Figure 10.28. (This device is popular in demonstrations among physicists, because it does unexpected things.) With the wheel rotating as shown, its angular momentum is to the woman's left. Suppose the person holding the wheel tries to rotate it as in the figure. Her natural expectation is that the wheel will rotate in the direction she pushes it—but what happens is quite different. The forces exerted create a torque that is horizontal toward the person, as shown in Figure 10.28(a). This torque creates a change in angular momentum in the same direction, perpendicular to the original angular momentum , thus changing the direction of but not the magnitude of . Figure 10.28 shows how and add, giving a new angular momentum with direction that is inclined more toward the person than before. The axis of the wheel has thus moved perpendicular to the forces exerted on it, instead of in the expected direction.  
FIGURE 10.27 In figure (a), the torque is perpendicular to the plane formed by  and  and is the direction your right thumb would point to if you curled your fingers in the direction of . Figure (b) shows that the direction of the torque is the same as that of the angular momentum it produces.

  
FIGURE 10.28 In figure (a), a person holding the spinning bike wheel lifts it with her right hand and pushes down with her left hand in an attempt to rotate the wheel. This action creates a torque directly toward her. This torque causes a change in angular momentum  in exactly the same direction. Figure (b) shows a vector diagram depicting how and add, producing a new angular momentum pointing more toward the person. The wheel moves toward the person, perpendicular to the forces she exerts on it.

This same logic explains the behavior of gyroscopes. Figure 10.29 shows the two forces acting on a spinning gyroscope. The torque produced is perpendicular to the angular momentum, thus the direction of the torque is changed, but not its magnitude. The gyroscope precesses around a vertical axis, since the torque is always horizontal and perpendicular to . If the gyroscope is not spinning, it acquires angular momentum in the direction of the torque  ), and it rotates around a horizontal axis, falling over just as we would expect.

Earth itself acts like a gigantic gyroscope. Its angular momentum is along its axis and points at Polaris, the North Star. But Earth is slowly precessing (once in about 26,000 years) due to the torque of the Sun and the Moon on its nonspherical shape.  
FIGURE 10.29 As seen in figure (a), the forces on a spinning gyroscope are its weight and the supporting force from the stand. These forces create a horizontal torque on the gyroscope, which create a change in angular momentum that is also horizontal. In figure (b), and  add to produce a new angular momentum with the same magnitude, but different direction, so that the gyroscope precesses in the direction shown instead of falling over.

# CHECK YOUR UNDERSTANDING

Rotational kinetic energy is associated with angular momentum? Does that mean that rotational kinetic energy is a vector?

# Solution

No, energy is always a scalar whether motion is involved or not. No form of energy has a direction in space and you can see that rotational kinetic energy does not depend on the direction of motion just as linear kinetic energy is independent of the direction of motion.# Glossary

angular acceleration the rate of change of angular velocity with time   
angular momentum the product of moment of inertia and angular velocity   
change in angular velocity the difference between final and initial values of angular velocity   
kinematics of rotational motion describes the relationships among rotation angle, angular velocity, angular acceleration, and time   
law of conservation of angular momentum angular momentum is conserved, i.e., the initial angular momentum is equal to the final angular momentum when no external torque is applied to the system   
moment of inertia mass times the square of perpendicular distance from the rotation axis; for a point mass, it is  and, because any object can be built up from a collection of point masses, this relationship is the basis for all other moments of inertia   
right-hand rule direction of angular velocity ω and angular momentum L in which the thumb of your right hand points when you curl your fingers in the direction of the disk’s rotation   
rotational inertia resistance to change of rotation. The more rotational inertia an object has, the harder it is to rotate   
rotational kinetic energy the kinetic energy due to the rotation of an object. This is part of its total kinetic energy   
tangential acceleration the acceleration in a direction tangent to the circle at the point of interest in circular motion   
torque the turning effectiveness of a force   
work-energy theorem if one or more external forces act upon a rigid object, causing its kinetic energy to change from  to  , then the work  done by the net force is equal to the change in kinetic energy

# Section Summary

# 10.1 Angular Acceleration

• Uniform circular motion is the motion with a constant angular velocity  .   
• In non-uniform circular motion, the velocity changes with time and the rate of change of angular velocity (i.e. angular acceleration) is  Linear or tangential acceleration refers to changes in the magnitude of velocity but not its direction, given as  .   
• For circular motion, note that  , so that    
• The radius r is constant for circular motion, and so  . Thus,    
By definition,  . Thus,  or 

# 10.2 Kinematics of Rotational Motion

• Kinematics is the description of motion. • The kinematics of rotational motion describes the relationships among rotation angle, angular velocity, angular acceleration, and time. • Starting with the four kinematic equations we developed in the One-Dimensional Kinematics, we

can derive the four rotational kinematic equations (presented together with their translational   
counterparts) seen in Table 10.2.   
In these equations, the subscript 0 denotes initial values  and  are initial values), and the average angular velocity  and average velocity  are   
defined as follows:   
 and 

# 10.3 Dynamics of Rotational Motion: Rotational Inertia

• The farther the force is applied from the pivot, the greater is the angular acceleration; angular acceleration is inversely proportional to mass. If we exert a force  on a point mass that is at a distance  from a pivot point and because the force is perpendicular to  , an acceleration  is obtained in the direction of  . We can rearrange this equation such that  , and then look for ways to relate this expression to expressions for rotational quantities. We note that  , and we substitute this expression into  , yielding  Torque is the turning effectiveness of a force. In this case, because  is perpendicular to  , torque is simply  . If we multiply both sides of the equation above by  , we get torque on the lefthand side. That is,   
   
or   
   
The moment of inertia  of an object is the sum of   
 for all the point masses of which it is   
composed. That is,   
   
The general relationship among torque, moment of   
inertia, and angular acceleration is   
   
or   


# 10.4 Rotational Kinetic Energy: Work and Energy Revisited

• The rotational kinetic energy  for an object with a moment of inertia  and an angular velocity  is given by  Helicopters store large amounts of rotational kinetic energy in their blades. This energy must be put into the blades before takeoff and maintained until the end of the flight. The engines do not have enough power to simultaneously provide lift and put significant rotational energy into the blades. Work and energy in rotational motion are completely analogous to work and energy in translational motion.   
The equation for the work-energy theorem for rotational motion is, net 

# 10.5 Angular Momentum and Its Conservation

• Every rotational phenomenon has a direct translational analog , likewise angular momentum  can be defined as  • This equation is an analog to the definition of

linear momentum as  . The relationship between torque and angular momentum is   
net    
Angular momentum, like energy and linear   
momentum, is conserved. This universally   
applicable law is another sign of underlying unity in physical laws. Angular momentum is conserved when net external torque is zero, just as linear momentum is conserved when the net external force is zero.

# 10.6 Collisions of Extended Bodies in Two Dimensions

• Angular momentum  is analogous to linear momentum and is given by  . Angular momentum is changed by torque, following the relationship  Angular momentum is conserved if the net torque is zero  constant (net  or  (net  . This equation is known as the law of conservation of angular momentum, which may be conserved in collisions.

# 10.7 Gyroscopic Effects: Vector Aspects of Angular Momentum

Torque is perpendicular to the plane formed by  and and is the direction your right thumb would point if you curled the fingers of your right hand in the direction of . The direction of the torque is thus the same as that of the angular momentum it produces.   
The gyroscope precesses around a vertical axis, since the torque is always horizontal and perpendicular to . If the gyroscope is not spinning, it acquires angular momentum in the direction of the torque  ), and it rotates about a horizontal axis, falling over just as we would expect. Earth itself acts like a gigantic gyroscope. Its angular momentum is along its axis and points at Polaris, the North Star.

# Conceptual Questions

# 10.1 Angular Acceleration

1. Analogies exist between rotational and translational physical quantities. Identify the rotational term analogous to each of the following: acceleration, force, mass, work, translational kinetic energy, linear momentum, impulse.

2. Explain why centripetal acceleration changes the direction of velocity in circular motion but not its magnitude.   
3. In circular motion, a tangential acceleration can change the magnitude of the velocity but not its direction. Explain your answer.4. Suppose a piece of food is on the edge of a rotating microwave oven plate. Does it experience nonzero tangential acceleration, centripetal acceleration, or both when: (a) The plate starts to spin? (b) The plate rotates at constant angular velocity? (c) The plate slows to a halt?

# 10.3 Dynamics of Rotational Motion: Rotational Inertia

5. The moment of inertia of a long rod spun around an axis through one end perpendicular to its length is  . Why is this moment of inertia greater than it would be if you spun a point mass  at the location of the center of mass of the rod (at  )? (That would be  )   
6. Why is the moment of inertia of a hoop that has a mass  and a radius  greater than the moment of inertia of a disk that has the same mass and radius? Why is the moment of inertia of a spherical shell that has a mass  and a radius  greater than that of a solid sphere that has the same mass and radius?   
7. Give an example in which a small force exerts a large torque. Give another example in which a large force exerts a small torque.   
8. While reducing the mass of a racing bike, the greatest benefit is realized from reducing the mass of the tires and wheel rims. Why does this allow a racer to achieve greater accelerations than would an identical reduction in the mass of the bicycle’s frame?

  
FIGURE 10.30 The image shows a side view of a racing bicycle. Can you see evidence in the design of the wheels on this racing bicycle that their moment of inertia has been purposely reduced? (credit: Jesús Rodriguez)

9. A ball slides up a frictionless ramp. It is then rolled without slipping and with the same initial velocity up another frictionless ramp (with the same slope angle). In which case does it reach a greater height, and why?

# 10.4 Rotational Kinetic Energy: Work and Energy Revisited

10. Describe the energy transformations involved when a yo-yo is thrown downward and then climbs back up its string to be caught in the user’s hand.   
11. What energy transformations are involved when a dragster engine is revved, its clutch let out rapidly, its tires spun, and it starts to accelerate forward? Describe the source and transformation of energy at each step.   
12. The Earth has more rotational kinetic energy now than did the cloud of gas and dust from which it formed. Where did this energy come from?

  
FIGURE 10.31 An immense cloud of rotating gas and dust contracted under the influence of gravity to form the Earth and in the process rotational kinetic energy increased. (credit: NASA)

# 10.5 Angular Momentum and Its Conservation

13. When you start the engine of your car with the transmission in neutral, you notice that the car rocks in the opposite sense of the engine’s rotation. Explain in terms of conservation of angular momentum. Is the angular momentum of the car conserved for long (for more than a few seconds)?14. Suppose a child walks from the outer edge of a rotating merry-go round to the inside. Does the angular velocity of the merry-go-round increase, decrease, or remain the same? Explain your answer.

  
FIGURE 10.32 A child may jump off a merry-go-round in a variety of directions.

21. Jet turbines spin rapidly. They are designed to fly apart if something makes them seize suddenly, rather than transfer angular momentum to the plane’s wing, possibly tearing it off. Explain how flying apart conserves angular momentum without transferring it to the wing.

22. An astronaut tightens a bolt on a satellite in orbit. He rotates in a direction opposite to that of the bolt, and the satellite rotates in the same direction as the bolt. Explain why. If a handhold is available on the satellite, can this counter-rotation be prevented? Explain your answer.

23. Competitive divers pull their limbs in and curl up their bodies when they do flips. Just before entering the water, they fully extend their limbs to enter straight down. Explain the effect of both actions on their angular velocities. Also explain the effect on their angular momenta.

15. Suppose a child gets off a rotating merry-goround. Does the angular velocity of the merry-goround increase, decrease, or remain the same if: (a) He jumps off radially? (b) He jumps backward to land motionless? (c) He jumps straight up and hangs onto an overhead tree branch? (d) He jumps off forward, tangential to the edge? Explain your answers. (Refer to Figure 10.32).

16. Helicopters have a small propeller on their tail to keep them from rotating in the opposite direction of their main lifting blades. Explain in terms of Newton’s third law why the helicopter body rotates in the opposite direction to the blades.

17. Whenever a helicopter has two sets of lifting blades, they rotate in opposite directions (and there will be no tail propeller). Explain why it is best to have the blades rotate in opposite directions.

18. Describe how work is done by a skater pulling in her arms during a spin. In particular, identify the force she exerts on each arm to pull it in and the distance each moves, noting that a component of the force is in the direction moved. Why is angular momentum not increased by this action?

  
FIGURE 10.33 The diver spins rapidly when curled up and slows when she extends her limbs before entering the water.

19. When there is a global heating trend on Earth, the atmosphere expands and the length of the day increases very slightly. Explain why the length of a day increases.

20. Nearly all conventional piston engines have flywheels on them to smooth out engine vibrations caused by the thrust of individual piston firings. Why does the flywheel have this effect?

24. Draw a free body diagram to show how a diver gains angular momentum when leaving the diving board.25. In terms of angular momentum, what is the advantage of giving a football or a rifle bullet a spin when throwing or releasing it?

  
FIGURE 10.34 The image shows a view down the barrel of a cannon, emphasizing its rifling. Rifling in the barrel of a canon causes the projectile to spin just as is the case for rifles (hence the name for the grooves in the barrel). (credit: Elsie esq., Flickr)

# 10.6 Collisions of Extended Bodies in Two Dimensions

26. Describe two different collisions—one in which angular momentum is conserved, and the other in which it is not. Which condition determines whether or not angular momentum is conserved in a collision?

27. Suppose an ice hockey puck strikes a hockey stick that lies flat on the ice and is free to move in any direction. Which quantities are likely to be conserved: angular momentum, linear momentum, or kinetic energy (assuming the puck and stick are very resilient)?   
28. While driving his motorcycle at highway speed, a physics student notices that pulling back lightly on the right handlebar tips the cycle to the left and produces a left turn. Explain why this happens.

# 10.7 Gyroscopic Effects: Vector Aspects of Angular Momentum

29. While driving his motorcycle at highway speed, a physics student notices that pulling back lightly on the right handlebar tips the cycle to the left and produces a left turn. Explain why this happens.

30. Gyroscopes used in guidance systems to indicate directions in space must have an angular momentum that does not change in direction. Yet they are often subjected to large forces and accelerations. How can the direction of their angular momentum be constant when they are accelerated?

# Problems & Exercises

# 10.1 Angular Acceleration

1. At its peak, a tornado is  in diameter and carries  winds. What is its angular velocity in revolutions per second?

2. Integrated Concepts An ultracentrifuge accelerates from rest to 100,000 rpm in  . (a) What is its angular acceleration in  (b) What is the tangential acceleration of a point  from the axis of rotation? (c) What is the radial acceleration in  and multiples of  of this point at full rpm?

3. Integrated Concepts You have a grindstone (a disk) that is  , has a  radius, and is turning at 90.0 rpm, and you press a steel axe against it with a radial force of  . (a) Assuming the kinetic coefficient of friction between steel and stone is 0.20, calculate the angular acceleration of the grindstone. (b) How many turns will the stone make before coming to rest?

4. Unreasonable Results

You are told that a basketball player spins the ball with an angular acceleration of  . (a) What is the ball’s final angular velocity if the ball starts from rest and the acceleration lasts  (b) What is unreasonable about the result? (c) Which premises are unreasonable or inconsistent?

# 10.2 Kinematics of Rotational Motion

5. With the aid of a string, a gyroscope is accelerated from rest to  in  . (a) What is its angular acceleration in  (b) How many revolutions does it go through in the process?   
6. Suppose a piece of dust finds itself on a CD. If the spin rate of the CD is 500 rpm, and the piece of dust is  from the center, what is the total distance traveled by the dust in 3 minutes? (Ignore accelerations due to getting the CD rotating.)7. A gyroscope slows from an initial rate of  at a rate of  . (a) How long does it take to come to rest? (b) How many revolutions does it make before stopping?

8. During a very quick stop, a car decelerates at  . (a) What is the angular acceleration of its  - radius tires, assuming they do not slip on the pavement? (b) How many revolutions do the tires make before coming to rest, given their initial angular velocity is 95.0 rad/s? (c) How long does the car take to stop completely? (d) What distance does the car travel in this time? (e) What was the car’s initial velocity? (f) Do the values obtained seem reasonable, considering that this stop happens very quickly?

  
FIGURE 10.35 Yo-yos are amusing toys that display significant physics and are engineered to enhance performance based on physical laws. (credit: Beyond Neon, Flickr)

9. Everyday application: Suppose a yo-yo has a center shaft that has a 0.250 cm radius and that its string is being pulled.

(a) If the string is stationary and the yo-yo accelerates away from it at a rate of  , what is the angular acceleration of the yo-yo?

(b) What is the angular velocity after 0.750 s if it starts from rest?

(c) The outside radius of the yo-yo is  . What is the tangential acceleration of a point on its edge?

# 10.3 Dynamics of Rotational Motion: Rotational Inertia

10. This problem considers additional aspects of example Calculating the Effect of Mass Distribution on a Merry-Go-Round. (a) How long does it take the father to give the merry-go-round an angular velocity of  (b) How many revolutions must he go through to generate this velocity? (c) If he exerts a slowing force of  at a radius of  , how long would it take him to stop them?

11. Calculate the moment of inertia of a skater given the following information. (a) The  skater is approximated as a cylinder that has a  radius. (b) The skater with arms extended is approximately a cylinder that is  has a  radius, and has two  -long arms which are  each and extend straight out from the cylinder like rods rotated about their ends.

12. The triceps muscle in the back of the upper arm extends the forearm. This muscle in a professional boxer exerts a force of  with an effective perpendicular lever arm of  , producing an angular acceleration of the forearm of  . What is the moment of inertia of the boxer’s forearm?

13. A soccer player extends her lower leg in a kicking motion by exerting a force with the muscle above the knee in the front of her leg. She produces an angular acceleration of  and her lower leg has a moment of inertia of  . What is the force exerted by the muscle if its effective perpendicular lever arm is 

14. Suppose you exert a force of  tangential to a 0.280-m-radius  grindstone (a solid disk). (a)What torque is exerted? (b) What is the angular acceleration assuming negligible opposing friction? (c) What is the angular acceleration if there is an opposing frictional force of  exerted 1.50 cm from the axis?15. Consider the  motorcycle wheel shown in Figure 10.36. Assume it to be approximately an annular ring with an inner radius of  and an outer radius of  . The motorcycle is on its center stand, so that the wheel can spin freely. (a) If the drive chain exerts a force of  at a radius of  , what is the angular acceleration of the wheel? (b) What is the tangential acceleration of a point on the outer edge of the tire? (c) How long, starting from rest, does it take to reach an angular velocity of 80.0 rad/s?

  
FIGURE 10.36 A motorcycle wheel has a moment of inertia approximately that of an annular ring.

16. Zorch, an archenemy of Superman, decides to slow Earth’s rotation to once per  by exerting an opposing force at and parallel to the equator. Superman is not immediately concerned, because he knows Zorch can only exert a force of  (a little greater than a Saturn V rocket’s thrust). How long must Zorch push with this force to accomplish his goal? (This period gives Superman time to devote to other villains.) Explicitly show how you follow the steps found in Problem-Solving Strategy for Rotational Dynamics.

17. An automobile engine can produce  of torque. Calculate the angular acceleration produced if  of this torque is applied to the drive shaft, axle, and rear wheels of a car, given the following information. The car is suspended so that the wheels can turn freely. Each wheel acts like a  disk that has a  radius. The walls of each tire act like a  annular ring that has inside radius of  and outside radius of  . The tread of each tire acts like  hoop of radius  . The  axle acts like a rod that has a 2.00-cm radius. The  drive shaft acts like a rod that has a 3.20-cm radius.

18. Starting with the formula for the moment of inertia of a rod rotated around an axis through one end perpendicular to its length  , prove that the moment of inertia of a rod rotated about an axis through its center perpendicular to its length is  . You will find the graphics in Figure 10.11 useful in visualizing these rotations.

19. Unreasonable Results A gymnast doing a forward flip lands on the mat and exerts a  torque to slow their angular velocity to zero. Their initial angular velocity is  , and their moment of inertia is  . (a) What time is required for the gymnast to exactly stop their spin? (b) What is unreasonable about the result? (c) Which premises are unreasonable or inconsistent?

20. Unreasonable Results An advertisement claims that an  car is aided by its  flywheel, which can accelerate the car from rest to a speed of  s. The flywheel is a disk with a  radius. (a) Calculate the angular velocity the flywheel must have if  of its rotational energy is used to get the car up to speed. (b) What is unreasonable about the result? (c) Which premise is unreasonable or which premises are inconsistent?

# 10.4 Rotational Kinetic Energy: Work and Energy Revisited

21. This problem considers energy and work aspects of Example 10.7—use data from that example as needed. (a) Calculate the rotational kinetic energy in the merry-go-round plus child when they have an angular velocity of 20.0 rpm. (b) Using energy considerations, find the number of revolutions the father will have to push to achieve this angular velocity starting from rest. (c) Again, using energy considerations, calculate the force the father must exert to stop the merry-go-round in two revolutions

22. What is the final velocity of a hoop that rolls without slipping down a  -high hill, starting from rest?

23. (a) Calculate the rotational kinetic energy of Earth on its axis. (b) What is the rotational kinetic energy of Earth in its orbit around the Sun?

24. Calculate the rotational kinetic energy in the motorcycle wheel (Figure 10.36) if its angular velocity is 120 rad/s. Assume  ,   , and  .25. A baseball pitcher throws the ball in a motion where there is rotation of the forearm about the elbow joint as well as other movements. If the linear velocity of the ball relative to the elbow joint is  at a distance of  from the joint and the moment of inertia of the forearm is  , what is the rotational kinetic energy of the forearm?

26. While punting a football, a kicker rotates her leg about the hip joint. The moment of inertia of the leg is  and its rotational kinetic energy is 175 J. (a) What is the angular velocity of the leg? (b) What is the velocity of tip of the punter’s shoe if it is  from the hip joint? (c) Explain how the football can be given a velocity greater than the tip of the shoe (necessary for a decent kick distance).

27. A bus contains a  flywheel (a disk that has a  radius) and has a total mass of 10,000 kg. (a) Calculate the angular velocity the flywheel must have to contain enough energy to take the bus from rest to a speed of  , assuming  of the rotational kinetic energy can be transformed into translational energy. (b) How high a hill can the bus climb with this stored energy and still have a speed of  at the top of the hill? Explicitly show how you follow the steps in the Problem-Solving Strategy for Rotational Energy.

28. A ball with an initial velocity of  rolls up a hill without slipping. Treating the ball as a spherical shell, calculate the vertical height it reaches. (b) Repeat the calculation for the same ball if it slides up the hill without rolling.

29. While exercising in a fitness center, a man lies face down on a bench and lifts a weight with one lower leg by contacting the muscles in the back of the upper leg. (a) Find the angular acceleration produced given the mass lifted is  at a distance of  from the knee joint, the moment of inertia of the lower leg is  , the muscle force is 1500 N, and its effective perpendicular lever arm is  . (b) How much work is done if the leg rotates through an angle of  with a constant force exerted by the muscle?

30. To develop muscle tone, a woman lifts a  weight held in her hand. She uses her biceps muscle to flex the lower arm through an angle of  . (a) What is the angular acceleration if the weight is  from the elbow joint, her forearm has a moment of inertia of  and the net force she exerts is  at an effective perpendicular lever arm of  (b) How much work does she do?

31. Consider two cylinders that start down identical inclines from rest except that one is frictionless. Thus one cylinder rolls without slipping, while the other slides frictionlessly without rolling. They both travel a short distance at the bottom and then start up another incline. (a) Show that they both reach the same height on the other incline, and that this height is equal to their original height. (b) Find the ratio of the time the rolling cylinder takes to reach the height on the second incline to the time the sliding cylinder takes to reach the height on the second incline. (c) Explain why the time for the rolling motion is greater than that for the sliding motion.

32. What is the moment of inertia of an object that rolls without slipping down a  -high incline starting from rest, and has a final velocity of 6.00  Express the moment of inertia as a multiple of  , where  is the mass of the object and  is its radius.

33. Suppose a  motorcycle has two wheels like, the one described in Problem 10.15 and is heading toward a hill at a speed of  . (a) How high can it coast up the hill, if you neglect friction? (b) How much energy is lost to friction if the motorcycle only gains an altitude of  before coming to rest?

34. In softball, the pitcher throws with the arm fully extended (straight at the elbow). In a fast pitch the ball leaves the hand with a speed of  . (a) Find the rotational kinetic energy of the pitcher’s arm and ball together given that the arm's moment of inertia is  and the ball leaves the hand at a distance of  from the pivot at the shoulder. (b) What force did the muscles exert to cause the arm to rotate if their effective perpendicular lever arm is  and the ball is 0.156 kg?35. Construct Your Own Problem Consider the work done by a spinning skater pulling his arms in to increase his rate of spin. Construct a problem in which you calculate the work done with a “force multiplied by distance” calculation and compare it to the skater’s increase in kinetic energy.

# 10.5 Angular Momentum and Its Conservation

36. (a) Calculate the angular momentum of the Earth in its orbit around the Sun. (b) Compare this angular momentum with the angular momentum of Earth on its axis.

37. (a) What is the angular momentum of the Moon in its orbit around Earth? (b) How does this angular momentum compare with the angular momentum of the Moon on its axis? Remember that the Moon keeps one side toward Earth at all times. (c) Discuss whether the values found in parts (a) and (b) seem consistent with the fact that tidal effects with Earth have caused the Moon to rotate with one side always facing Earth.

38. Suppose you start an antique car by exerting a force of  on its crank for 0.250 s. What angular momentum is given to the engine if the handle of the crank is  from the pivot and the force is exerted to create maximum torque the entire time?

39. A playground merry-go-round has a mass of 120 kg and a radius of  and it is rotating with an angular velocity of 0.500 rev/s. What is its angular velocity after a  child gets onto it by grabbing its outer edge? The child is initially at rest.

40. Three children are riding on the edge of a merrygo-round that is  , has a  radius, and is spinning at 20.0 rpm. The children have masses of 22.0, 28.0, and  . If the child who has a mass of  moves to the center of the merrygo-round, what is the new angular velocity in rpm?

41. (a) Calculate the angular momentum of an ice skater spinning at 6.00 rev/s given his moment of inertia is  . (b) He reduces his rate of spin (his angular velocity) by extending his arms and increasing his moment of inertia. Find the value of his moment of inertia if his angular velocity decreases to 1.25 rev/s. (c) Suppose instead he keeps his arms in and allows friction of the ice to slow him to 3.00 rev/s. What average torque was exerted if this takes 

42. Construct Your Own Problem Consider the Earth-Moon system. Construct a problem in which you calculate the total angular momentum of the system including the spins of the Earth and the Moon on their axes and the orbital angular momentum of the Earth-Moon system in its nearly monthly rotation. Calculate what happens to the Moon’s orbital radius if the Earth’s rotation decreases due to tidal drag. Among the things to be considered are the amount by which the Earth’s rotation slows and the fact that the Moon will continue to have one side always facing the Earth.

# 10.6 Collisions of Extended Bodies in Two Dimensions

43. Repeat Example 10.15 in which the disk strikes and adheres to the stick  from the nail.

44. Repeat Example 10.15 in which the disk originally spins clockwise at 1000 rpm and has a radius of 1.50 cm.

45. Twin skaters approach one another as shown in Figure 10.37 and lock hands. (a) Calculate their final angular velocity, given each had an initial speed of  relative to the ice. Each has a mass of  , and each has a center of mass located  from their locked hands. You may approximate their moments of inertia to be that of point masses at this radius. (b) Compare the initial kinetic energy and final kinetic energy.

  
FIGURE 10.37 Twin skaters approach each other with identical speeds. Then, the skaters lock hands and spin.46. Suppose a 0.250-kg ball is thrown at  to a motionless person standing on ice who catches it with an outstretched arm as shown in Figure 10.38. (a) Calculate the final linear velocity of the person, given his mass is  . (b) What is his angular velocity if each arm is 5.00 kg? You may treat the ball as a point mass and treat the person's arms as uniform rods (each has a length of  ) and the rest of his body as a uniform cylinder of radius  . Neglect the effect of the ball on his center of mass so that his center of mass remains in his geometrical center. (c) Compare the initial and final total kinetic energies.

  
FIGURE 10.38 The figure shows the overhead view of a person standing motionless on ice about to catch a ball. Both arms are outstretched. After catching the ball, the skater recoils and rotates.

47. Repeat Example 10.15 in which the stick is free to have translational motion as well as rotational motion.

# 10.7 Gyroscopic Effects: Vector Aspects of Angular Momentum

# 48. Integrated Concepts

The axis of Earth makes a  angle with a   
direction perpendicular to the plane of Earth’s orbit. As shown in Figure 10.39, this axis   
precesses, making one complete rotation in   
25,780 y.   
(a) Calculate the change in angular momentum in half this time.   
(b) What is the average torque producing this change in angular momentum?   
(c) If this torque were created by a single force (it is not) acting at the most effective point on the equator, what would its magnitude be?

  
FIGURE 10.39 The Earth’s axis slowly precesses, always making an angle of  with the direction perpendicular to the plane of Earth’s orbit. The change in angular momentum for the two shown positions is quite large, although the magnitude is unchanged.