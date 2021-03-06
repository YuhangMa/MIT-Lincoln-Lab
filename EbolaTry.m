clear;
clc;

SimulationNUM = 10;
population = 200;
timestep = 50;

beta_I = 0.16;
beta_H = 0.062;
beta_F = 0.489;
Incubation = 12;
InfDur = 15;
TimeToHosp = 3.24;
TimeInfDeath = 13.31;
TimeHospDeath = 10.07;
TimeHospRec = 15.88;
DurFun = 2.01;

% Transition matrix [S E I H F R D]
Tran = [0.5 0.5 0 0 0 0 0; 
      0 1-1/Incubation 1/Incubation 0 0 0 0
      0 0 1/InfDur 1/TimeToHosp 1/TimeInfDeath 1-1/InfDur-1/TimeToHosp-1/TimeInfDeath 0; 
      0 0 0 1-1/TimeHospDeath-1/TimeHospRec 1/TimeHospDeath 1/TimeHospRec 0; 
      0 0 0 0 1/DurFun 0 1-1/DurFun; 
      0 0 0 0 0 1 0; 
      0 0 0 0 0 0 1];

final_S = zeros(1,SimulationNUM);
final_R = zeros(1,SimulationNUM);
final_D = zeros(1,SimulationNUM);


for s = 1:SimulationNUM

people = [1 zeros(1,population-1)]; % initialization 

c0=zeros(1,timestep);
c1=zeros(1,timestep);
c2=zeros(1,timestep);
c3=zeros(1,timestep);
c4=zeros(1,timestep);
c5=zeros(1,timestep);
c6=zeros(1,timestep);

a0 = sum(people == 0); %compute how many people are 0 at timestep 1
a1 = sum(people == 1); %compute how many people are 1 at timestep 1
a2 = sum(people == 2); %compute how many people are 2 at timestep 1
a3 = sum(people == 3); %compute how many people are 3 at timestep 1
a4 = sum(people == 4); %compute how many people are 4 at timestep 1
a5 = sum(people == 5); %compute how many people are 5 at timestep 1
a6 = sum(people == 6); %compute how many people are 6 at timestep 1

c0(1)=a0;
c1(1)=a1;
c2(1)=a2;
c3(1)=a3;
c4(1)=a4;
c5(1)=a5;
c6(1)=a6;

SroE = zeros(1,timestep);

for t=2:timestep

d0=0; %change of amount
d1=0;
d2=0;
d3=0;
d4=0;
d5=0;
d6=0;    
    
StoE(t) = (beta_I*c2(t-1)+beta_H*c3(t-1)+beta_F*c4(t-1))/population;

for i=1:population
    
r=rand(1,population); %comparison vector
    
    
    if people(i)==0     % S goes to S or E
        if r(i)<=StoE(t)
            people(i)=1;
            d1=d1+1;
            d0=d0-1;
        end
    elseif people(i)==1 % E goes to E or I 
        if r(i)<=Tran(2,3)
            people(i)=2;
            d2=d2+1;
            d1=d1-1;
        end
    elseif people(i)==2 % I goes to I, H, F or R
        if r(i)<=Tran(3,4)
            people(i)=3;
            d3=d3+1;
            d2=d2-1;
        elseif Tran(3,4)<r(i)<=Tran(3,4)+Tran(3,5)
            people(i)=4;
            d4=d4+1;
            d2=d2-1;
        elseif Tran(3,4)+Tran(3,5)<r(i)<=Tran(3,4)+Tran(3,5)+Tran(3,6)
            people(i)=5;
            d5=d5+1;
            d2=d2-1;
        end
    elseif people(i)==3 % H goes to H, F or R
        if r(i)<=Tran(4,5)
            people(i)=4;
            d4=d4+1;
            d3=d3-1;
        elseif Tran(4,5)<r(i)<=Tran(4,5)+Tran(4,6) 
            people(i)=5;
            d5=d5+1;
            d3=d3-1;
        end
    elseif people(i)==4 % F goes to F or D
        if r(i)<=Tran(5,7)
            people(i)=6;
            d6=d6+1;
            d4=d4-1;
        end
        
    end  
    
    c0(1,t) = c0(1,t-1) + d0;
    c1(1,t) = c1(1,t-1) + d1;
    c2(1,t) = c2(1,t-1) + d2;
    c3(1,t) = c3(1,t-1) + d3;
    c4(1,t) = c4(1,t-1) + d4;
    c5(1,t) = c5(1,t-1) + d5;
    c6(1,t) = c6(1,t-1) + d6;
    
end
people;
end

people;
SUM_OF_PEOPLE = sum(c0(1,timestep)+c1(1,timestep)+c2(1,timestep)+c3(1,timestep)+c4(1,timestep)+c5(1,timestep)+c6(1,timestep));


 figure
 subplot(4,2,[1,2]);
 plot(c0/population,'LineWidth',2)
 axis([1 timestep 0 1])
 title('Proportion of S State')
 
 subplot(4,2,3);
 plot(c1/population,'LineWidth',2)
 axis([1 timestep 0 1])
 title('Proportion of E State')
 
 subplot(4,2,4);
 plot(c2/population,'LineWidth',2)
 axis([1 timestep 0 1])
 title('Proportion of I State')
 
 subplot(4,2,5);
 plot(c3/population,'LineWidth',2)
 axis([1 timestep 0 1])
 title('Proportion of H State')
 
 subplot(4,2,6);
 plot(c4/population,'LineWidth',2)
 axis([1 timestep 0 1])
 title('Proportion of F State')
 
 subplot(4,2,7);
 plot(c5/population,'LineWidth',2)
 axis([1 timestep 0 1])
 title('Proportion of R State')
 
 subplot(4,2,8);
 plot(c6/population,'LineWidth',2)
 axis([1 timestep 0 1])
 title('Proportion of D State')


final_S(s) = c0(timestep)/population;
final_R(s) = c5(timestep)/population;
final_D(s) = c6(timestep)/population;

end

final_S
final_R
final_D

% to compute the mean
% A = 1 - final_S
% for i = 1:100
%     if A(i) < 0.1
%         A(i)=0
%     end
% end
% A(A==0) = [];
% mean(A)



