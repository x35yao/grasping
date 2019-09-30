% Object can be 'foambrick', 'mustard', 'softscrub' or 'sugarbox'
object = 'foambrick';

switch object
    case 'softscrub'
        % Import an STL mesh, returning a PATCH-compatible face-vertex structure
        obj = read_wobj('softscrub.obj');
        % Translation and roll of object (degrees)
        % Rendering of mesh shifts the object's orientation and centre of the object's base from the origin 
        move = [-0.012652, -0.0018937, 0];
        roll = -33;
        arrowsize = 0.2;
        factor = 2;
        color = [1 1 1];
        % Read coordinates from file
        coordinates = csvread('softscrub_transformed_object_coordinates.csv',1);
    case 'foambrick'
        % Import an STL mesh, returning a PATCH-compatible face-vertex structure
        obj = read_wobj('foambrick.obj');
        % Translation and roll of object (degrees)
        move = [-0.0099107, -0.0048833, 0];
        roll = 22;
        arrowsize = 20;
        color = [128/255 0 0];
        factor = 0.5;
        % Read coordinates from file
        %coordinates = csvread('897027_ray_coordinates.csv',1);
    case 'mustard'
        % Import an STL mesh, returning a PATCH-compatible face-vertex structure
        obj = read_wobj('mustard.obj');
        % Translation and roll of object (degrees)
        move = [0.0042344, -0.0099301, 0];
        roll = -39;
        arrowsize = 2;
        factor = 2;
        color = [1 1 0]; %yellow
        % Read coordinates from file
        coordinates = csvread('mustard_transformed_object_coordinates.csv',1);
    case 'sugarbox'
        % Import an STL mesh, returning a PATCH-compatible face-vertex structure
        obj = read_wobj('sugarbox.obj');
        % Translation and roll of object (degrees)
        move = [-0.008986, 0.00022655, 0];
        roll = 52;
        arrowsize = 0.05;
        factor = 0.1;
        color = [199 236 147]./255;
        % Read coordinates from file
        coordinates = csvread('sugarbox_transformed_object_coordinates.csv',1);
end


figure;
% Creates the rendering of the  mesh

tval=obj.vertices(:,3);
box = patch('vertices',obj.vertices,'faces',obj.objects.data.vertices,'FaceVertexCData', tval,'FaceColor',color);

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
% Coordinates of gripper with translation of mesh added



hold on;

origin = [-0.05,0,0.04];
dir = [0.02,-0.01,0];
tree = getAABBTree(obj);
a = tree.getIntersections(origin,dir);
res = toArray(a);
data = cell(res);
num_interc = length(data)
for m = 1:num_interc
    c = data{m};
    d(m) = sqrt((origin(1)-c(1))^2+(origin(2)-c(2))^2+(origin(3)-c(3))^2);
end


