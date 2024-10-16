function save_signals_to_excel(data_folder)
    % Function to load signal data from .mat files in a specified folder
    % and save it to Excel, with different sheets for each signal type.

    % Load STN_LFP data
    load(fullfile(data_folder, 'STN_LFP.mat'));
    stn_signal = block.segments{1, 1}.analogsignals{1, 1}.signal;
    stn_signal = stn_signal(:);  % Ensure column vector

    % Load Cortical_Soma_v data
    load(fullfile(data_folder, 'Cortical_Pop', 'Cortical_Soma_v.mat'));
    cortical_soma_signal = block.segments{1, 1}.analogsignals{1, 1}.signal;

    % Load Cortical_Collateral_v data
    load(fullfile(data_folder, 'Cortical_Pop', 'Cortical_Collateral_v.mat'));
    cortical_collateral_signal = block.segments{1, 1}.analogsignals{1, 1}.signal;

    % Extract the folder name to use as the Excel file name
    [~, folder_name] = fileparts(data_folder);

    % Construct the full Excel file name
    excel_file_name = strcat(folder_name, '.xlsx');
    
    % Write STN signal to Excel in its own sheet
    writematrix(stn_signal, excel_file_name, 'Sheet', 'STN_LFP', 'Range', 'A1');
    
    % Write all Cortical Soma signals to one sheet, each column in the array as a column in Excel
    writematrix(cortical_soma_signal, excel_file_name, 'Sheet', 'Cortical_Soma', 'Range', 'A1');
    
    % Write all Cortical Collateral signals to one sheet, each column in the array as a column in Excel
    writematrix(cortical_collateral_signal, excel_file_name, 'Sheet', 'Cortical_Collateral', 'Range', 'A1');
    
    disp(['Signals saved to Excel file: ', excel_file_name]);
end
