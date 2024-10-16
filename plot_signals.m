function plot_signals(data_folder)
    % Function to plot signals from .mat files in a specified folder
    % It plots STN_LFP and either ctx_Signal or DBS_Signal based on the folder name.

    % Load and plot STN_LFP signal
    load(fullfile(data_folder, 'STN_LFP.mat'));
    figure;
    plot(block.segments{1, 1}.analogsignals{1, 1}.signal);
    xlabel('Time ms');
    ylabel('Voltage mV');
    title('STN LFP');
    disp('STN LFP plotted.');

    % Determine if the folder name contains 'ctx' or 'DBS' and plot accordingly
    if contains(data_folder, 'ctx', 'IgnoreCase', true)
        % Load and plot Cortex Stimulation Current signal
        load(fullfile(data_folder, 'ctx_Signal.mat'));
        figure;
        plot(block.segments{1, 1}.analogsignals{1, 1}.signal);
        xlabel('Time ms');
        ylabel('Current mA');
        title('Cortex Stimulation Current');
        disp('Cortex Stimulation Current plotted.');
    elseif contains(data_folder, 'DBS', 'IgnoreCase', true)
        % Load and plot DBS Stimulation Current signal
        load(fullfile(data_folder, 'DBS_Signal.mat'));
        figure;
        plot(block.segments{1, 1}.analogsignals{1, 1}.signal);
        xlabel('Time ms');
        ylabel('Current mA');
        title('DBS Stimulation Current');
        disp('DBS Stimulation Current plotted.');
    else
        disp('Neither Cortex nor DBS Signal found in the folder name. No additional plots.');
    end
end