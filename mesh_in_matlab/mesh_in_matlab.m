% Object can be 'foambrick', 'mustard', 'softscrub' or 'sugarbox'
object = 'sugarbox';

switch object
    case 'softscrub'
        % Import an STL mesh, returning a PATCH-compatible face-vertex structure
        obj = read_wobj('softscrub.obj');
        % Translation and roll of object (degrees)
        % Rendering of mesh shifts the object's orientation and centre of the object's base from the origin 
        move = [-0.012652, -0.0018937, 0];
        roll = -33;
        arrowsize = 0.05;
        factor = 2;
        color = [1 1 1];
        % Read coordinates from file
        coordinates = csvread('softscrub_gripper_wrt_object.csv',1);
    case 'foambrick'
        % Import an STL mesh, returning a PATCH-compatible face-vertex structure
        obj = read_wobj('foambrick.obj');
        % Translation and roll of object (degrees)
        move = [-0.0099107, -0.0048833, 0];
        roll = 22;
        arrowsize = 0.2;
        color = [128/255 0 0];
        factor = 5;
        % Read coordinates from file
        coordinates = csvread('foambrick_gripper_wrt_object.csv',1);
    case 'mustard'
        % Import an STL mesh, returning a PATCH-compatible face-vertex structure
        obj = read_wobj('mustard.obj');
        % Translation and roll of object (degrees)
        move = [0.0042344, -0.0099301, 0];
        roll = -39;
        arrowsize = 0.2;
        factor = 2;
        color = [1 1 0]; %yellow
        % Read coordinates from file
        coordinates = csvread('mustard_gripper_wrt_object.csv',1);
    case 'sugarbox'
        % Import an STL mesh, returning a PATCH-compatible face-vertex structure
        obj = read_wobj('sugarbox.obj');
        % Translation and roll of object (degrees)
        move = [-0.008986, 0.00022655, 0];
        roll = 52;
        arrowsize = 0.1;
        factor = 0.1;
        color = [199 236 147]./255;
        % Read coordinates from file
        coordinates = csvread('sugarbox_gripper_wrt_object.csv',1);
end
%%
figure;
% Creates the rendering of the  mesh

tval=obj.vertices(:,3);
box = patch('vertices',obj.vertices,'faces',obj.objects.data.vertices,'FaceVertexCData', tval,'FaceColor',color);
%%
% Add a camera light, and tone down the specular highlighting
camlight('headlight');
material('dull');

% Fix the axes scaling, and set a nice view angle
axis('image');
ax=gca;
xlabel('x')
ylabel('y')
zlabel('z')
% legend('','z', 'y', 'x')

switch object
    case 'sugarbox'
        axis([-7 6 -4.5 4.5 0 20]./100);
    case 'foambrick'
        axis([-5 3 -5.2 4.3 0 20]./100);
    case 'softscrub'
        axis([-6 5 -6 6 0 26]./100);
    case 'mustard'
        axis([-5 5.5 -6 4 0 20]./100);
end
%%
% Coordinates of gripper with translation of mesh added
x_gripper = coordinates(:,2)./100 ;
y_gripper = coordinates(:,3)./100 ;
z_gripper = coordinates(:,4)./100;

% Vector denoting z axis of gripper
Zx = coordinates(:,6)./100 ;
Zy = coordinates(:,7)./100 ;
Zz = coordinates(:,8)./100;
% Vector denoting y axis of gripper
Yx = coordinates(:,10)./100 ;
Yy = coordinates(:,11)./100;
Yz = coordinates(:,12)./100;
% Vector denoting x axis of gripper
Xx = coordinates(:,14)./100 ;
Xy = coordinates(:,15)./100 ;
Xz = coordinates(:,16)./100;
% %%
% box = patch('vertices',obj.vertices,'faces',obj.objects.data.vertices,'FaceVertexCData', tval,'FaceColor',color);
% 
% arrowsize = 5;
% n = 91
% hold on;
% 
%  quiver3(x_gripper(n), y_gripper(n), z_gripper(n), Zx(n), Zy(n), Zz(n), arrowsize, 'Color','b','LineWidth',0.4);
% %%
hold on;
quiver3(x_gripper, y_gripper, z_gripper, Zx, Zy, Zz, arrowsize, 'Color','B','LineWidth', 0.4)
hold on;
quiver3(x_gripper, y_gripper, z_gripper, Yx, Yy, Yz, arrowsize, 'Color','r','LineWidth', 0.4)
hold on;
quiver3(x_gripper, y_gripper, z_gripper, Xx, Xy, Xz, arrowsize, 'Color','g','LineWidth', 0.4)

switch object
    case 'sugarbox'
        axis([-12 12 -12 12 0 20]./100);
    case 'foambrick'
        axis([-10 10 -10 10 0 20]./100);
    case 'softscrub'
        axis([-12 12 -11 11 0 26]./100);
    case 'mustard'
        axis([-11 11 -11 11 0 20]./100);
end

xlabel('x')
ylabel('y')
zlabel('z')
% legend('','z', 'y', 'x')

% Shadowing
for i=1:length(x_gripper)
    hold on;
    % Add a patch
    v = [x_gripper(i) y_gripper(i) 0;
         x_gripper(i)+ factor*arrowsize*Zx(i) y_gripper(i)+factor*arrowsize*Zy(i) 0;
         x_gripper(i)+ factor*arrowsize*Zx(i) y_gripper(i)+factor*arrowsize*Zy(i)+0.0001 0;
         x_gripper(i) y_gripper(i)+0.0001 0];
     f = [1 2 3 4];
    gray = [0.3 0.3 0.3];
    patch('Faces', f, 'Vertices', v ,'FaceColor', gray)
    % The order of the "children" of the plot determines which one appears on top.
    % I need to flip it here.
    set(gca,'children',flipud(get(gca,'children')))
end

