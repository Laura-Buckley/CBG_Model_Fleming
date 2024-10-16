% Laura Buckley 09/2024
% Script to handle the simulation results:
%   complete the initial plots -checking the DBS / CTX stimulation is correclty applied
%   saving the STN LFP data and voltage data to an excel file named
%   appropriately 

% Plot signals - check correct stimulus was applied 
%plot_signals(data_folder);

% Specify the data folder names as a string array
files1 = [
    "simulation-results-ctx-60Hz-100uA-long-sim-dist-check",];

% Loop through each folder
for i = 1:length(files1)
    data_folder = files1(i);
    
    % Call the function to save signals to Excel
    save_signals_to_excel(data_folder);
end
