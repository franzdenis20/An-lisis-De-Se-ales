
a = arduino;
function varargout = arduino(varargin)

% ARDUINO MATLAB code for Arduino.fig
%      ARDUINO, by itself, creates a new ARDUINO or raises the existing
%      singleton*.
%
%      H = ARDUINO returns the handle to a new ARDUINO or the handle to
%      the existing singleton*.
%
%      ARDUINO('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in ARDUINO.M with the given input arguments.
%
%      ARDUINO('Property','Value',...) creates a new ARDUINO or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Arduino_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Arduino_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Arduino

% Last Modified by GUIDE v2.5 19-Dec-2024 13:05:17

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Arduino_OpeningFcn, ...
                   'gui_OutputFcn',  @Arduino_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before Arduino is made visible.
function Arduino_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Arduino (see VARARGIN)

% Choose default command line output for Arduino
handles.output = hObject;
set(handles.Puerto,'string',handles.a.Port);
set(handles.Placa,'string',handles.a.Board);
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

end

% UIWAIT makes Arduino wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = Arduino_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

end


% --- Executes during object creation, after setting all properties.
function Placa_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Placa (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

end
% --- Executes during object creation, after setting all properties.
function Puerto_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Puerto (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
end

% --- Executes on button press in LED.
function LED_Callback(hObject, eventdata, handles)

v = get(hObject,'value');
    if v == 1

        writeDigitalPin(handles.a,'D3',1);
    else 
        writeDigitalPin(handles.a,'D3',0);
    end
end



% hObject    handle to LED (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of LED


% --- Executes during object creation, after setting all properties.
function LED_CreateFcn(hObject, eventdata, handles)
% hObject    handle to LED (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
end
clear handles.a;
delete(hObject);

