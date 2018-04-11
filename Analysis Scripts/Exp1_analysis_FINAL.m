%%#########################################################################
% SSEP analysis of Exp 1 EEG data
% Script organised into MATLAB cells to facilitate analysis.
% Complete analysis pipeline for study in MATLAB. Requires EEGLAB and the filterFGX function.
% Courtney Hilton, 2018. The University of Sydney.
%##########################################################################

%% constants

DATA_PATH = '/Users/Stilts/MATLAB/data/Exp1_data/Raw/';
EEGLAB_PATH =  '/Users/Stilts/MATLAB/toolboxes/eeglab14_1_1b'; %EEGLAB_PATH =  '/Users/Stilts/MATLAB/toolboxes/eeglab13_6_5b';
RESULTS_PATH = '/Users/Stilts/MATLAB/data/Exp1_data/Processed/';
eeglab
% Analysis parameters ### do I need these here?? or in RESS cell?

FILTER_LOWER_EDGE = 1;
FILTER_UPPER_EDGE = 25;
EPOCH_LENGTH = [1 33];
REFERENCE = []; %average reference

%% ++++++++++++++ PART 1: CONVERT VHDR FILES TO SETS ++++++++++++++ %%
%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%
%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%

% get everything ready (paths, eeglab, current directory, etc.)
% addpath(genpath(EEGLAB_PATH));
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
cd (DATA_PATH);
currentDir = (DATA_PATH);

% get the files in the directory and count how many there are
vhdrFilesinDir=dir(fullfile(currentDir,'*.vhdr'));
nVhdrFiles=length(vhdrFilesinDir);

%convert to .set file
    for vhdrfile = 1:nVhdrFiles  % iterate through vhdr files in data directory 
        vhdrName=(vhdrFilesinDir(vhdrfile).name); % output name of vhdr file including extension
        vhdrLocation=strcat(currentDir,vhdrName); % output path of vhdr file
        [~,setName] = fileparts(vhdrLocation); % output name of vhdr file WITHOUT extension
        EEG = pop_loadbv(currentDir, vhdrName); 
        [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, CURRENTSET,'setname',setName,'gui','off'); % creating new dataset and updating ALLEEG and current DATASET
        EEG.comments = pop_comments(EEG.comments,'','Dataset was converted from .vhdr/.eeg to .set format.',1);
        [ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET); % saving this
        EEG = eeg_checkset( EEG ); % checking for consistency
        finalLoc = strcat(RESULTS_PATH,setName); % creating path for this
        [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, CURRENTSET,'savenew',finalLoc,'overwrite','on','gui','off'); 
    end; 

%% ++++++++++++++ PART 2: PREPROCESS WHOLE EEG DATASETS ++++++++++++++ %%
%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%
%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%

% static locations
datapath = '/Users/Stilts/MATLAB/data/Exp1_data/Processed/Part_1/'; % location of the set files
resultspath = '/Users/Stilts/MATLAB/data/Exp1_data/Processed/Part_2/';

% get everything ready (paths, eeglab, current directory, etc.)
    cd (datapath);
    currentDir = (datapath);
    
    setFilesinDir=dir(fullfile(currentDir,'*.set'));
    nSetFiles=length(setFilesinDir);
    stimCodes = {  'E  1' 'E  2' 'E  3' 'E  4' 'E  5' 'E  6' 'E  7' 'E  8' }; % all stim codes
    stimTimePeriod = [-0.1           33.1]; % slightly wider than trial period for first pass
    %stimBaselinePeriod = [-200    0];    ##### opting to not baseline
    %correct here for now
    
     % main file loop
     for setfile = 1:nSetFiles % iterate through set files
            loadSet=(setFilesinDir(setfile).name); % Set with extension name
            setLocation=strcat(currentDir,loadSet);
            [~,setName] = fileparts(setLocation); % output name of set file WITHOUT extension
            % load set file
            EEG = pop_loadset('filename',setLocation);
            % High pass filter 
            EEG = pop_eegfiltnew(EEG, [], FILTER_LOWER_EDGE, [], true, [], 0); 
            EEG.comments = pop_comments(EEG.comments,'','High pass filter applied with lower edge of 0.8Hz',1); % SOFT CODED COMMENT~!!!!
            % Low pass filter
            EEG = pop_eegfiltnew(EEG, [], FILTER_UPPER_EDGE, [], 0, [], 0);
            EEG.comments = pop_comments(EEG.comments,'','Low pass filter applied with upper edge of 30Hz',1);
            % Create all epochs
            EEG = pop_epoch( EEG, stimCodes, stimTimePeriod, 'newname', strcat(setName,'_allepochs'));
            % reference to average electrodes
            EEG = pop_reref( EEG, [] );
            EEG.comments = pop_comments(EEG.comments,'','Average rereference',1);
            %run ICA
            %EEG = pop_runica(EEG, 'extended',1,'interupt','on');
            %EEG.comments = pop_comments(EEG.comments,'','ICA, runica',1);
            % Save new epochs
            fileName = strcat(setName,'_all_epochs.set');
            EEG = pop_saveset( EEG,'filename', strcat(setName,'_allepochs'),'filepath',resultspath);
     end;
 
%% +++++++++++++++++++ PART 3: CUT UP EPOCHS +++++++++++++++++++++++ %%
%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%
%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%

     datapath = '/Users/Stilts/MATLAB/data/Exp1_data/Processed/Part_2/'; 
     resultspath = '/Users/Stilts/MATLAB/data/Exp1_data/Processed/Part_3/';
     cd (datapath);
     currentDir = (datapath);
     EPOCH_LENGTH = [1 33]; % removing first second to avoid transient onset activity
     
     setFilesinDir=dir(fullfile(currentDir,'*.set'));
     nSetFiles=length(setFilesinDir);
     
     for setfile = 1:nSetFiles
         loadSet=(setFilesinDir(setfile).name);
         setLocation=strcat(currentDir,loadSet);
         [~,setName] = fileparts(setLocation); % output name of set file WITHOUT extension
         
         % make directory for each participant
         mkdir(resultspath, setName(1:6)); % 1-6 of set name is to get rid of 'all_epochs' bit
         subjectDir = strcat(resultspath,setName(1:6),'/');
         
         % load set file
         EEG = pop_loadset('filename',setLocation);
         
         % create control epochs
         EEG = pop_epoch( EEG, { 'E  1' }, EPOCH_LENGTH, 'newname', strcat(setName(1:6), '_control'));
         %EEG = pop_rmbase( EEG, BASELINE_CORRCTION);
         EEG = pop_saveset( EEG,'filename',strcat(setName(1:6), '_control'),'filepath',subjectDir);
         EEG = pop_loadset('filename',setLocation); % re-loads the all epochs set for next epoching
         
         % create word 2 epochs
         EEG = pop_epoch( EEG, { 'E  3' }, EPOCH_LENGTH, 'newname', strcat(setName(1:6), '_word2'));
         %EEG = pop_rmbase( EEG, BASELINE_CORRCTION);
         EEG = pop_saveset( EEG,'filename',strcat(setName(1:6), '_word2'),'filepath',subjectDir);
         EEG = pop_loadset('filename',setLocation);
         
         % create word 3 epochs
         EEG = pop_epoch( EEG, { 'E  4' }, EPOCH_LENGTH, 'newname', strcat(setName(1:6), '_word3'));
         %EEG = pop_rmbase( EEG, BASELINE_CORRCTION);
         EEG = pop_saveset( EEG,'filename',strcat(setName(1:6), '_word3'),'filepath',subjectDir);
         EEG = pop_loadset('filename',setLocation);
         
         % create imag2 epochs
         EEG = pop_epoch( EEG, { 'E  5' }, EPOCH_LENGTH, 'newname', strcat(setName(1:6), '_imag2'));
         %EEG = pop_rmbase( EEG, BASELINE_CORRCTION);
         EEG = pop_saveset( EEG,'filename',strcat(setName(1:6), '_imag2'),'filepath',subjectDir);
         EEG = pop_loadset('filename',setLocation);
         
         % create imag3 epochs
         EEG = pop_epoch( EEG, { 'E  6' }, EPOCH_LENGTH, 'newname', strcat(setName(1:6), '_imag3'));
         %EEG = pop_rmbase( EEG, BASELINE_CORRCTION);
         EEG = pop_saveset( EEG,'filename',strcat(setName(1:6), '_imag3'),'filepath',subjectDir);
         EEG = pop_loadset('filename',setLocation);
         
         % create gest2 epochs
         EEG = pop_epoch( EEG, { 'E  7' }, EPOCH_LENGTH, 'newname', strcat(setName(1:6), '_gest2'));
         %EEG = pop_rmbase( EEG, BASELINE_CORRCTION);
         EEG = pop_saveset( EEG,'filename',strcat(setName(1:6), '_gest2'),'filepath',subjectDir);
         EEG = pop_loadset('filename',setLocation);
         
         % create gest2 epochs
         EEG = pop_epoch( EEG, { 'E  8' }, EPOCH_LENGTH, 'newname', strcat(setName(1:6), '_gest3'));
         %EEG = pop_rmbase( EEG, BASELINE_CORRCTION);
         EEG = pop_saveset( EEG,'filename',strcat(setName(1:6), '_gest3'),'filepath',subjectDir);
     end;
     
%% ++++++++++++++ PART 4: AVERAGE ELECTRODE ANALYSIS ++++++++++++++ %%
%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%
%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%


nBins = 2; % setting bins for freq-domain normalization

% FFT parameters
freqRes = EEG.srate/EEG.pnts;
nfft = ceil( EEG.srate/freqRes);
hz    = linspace(0,EEG.srate,nfft);

%====================================================%
%============= initializing structures ==============%
%====================================================%


% Make directory to save results
%mkdir(resultspath, setName(1:6));
mkdir(resultspath, 'All_electrodes');
mkdir(resultspath, 'RESS');
mkdir(resultspath, strcat('Conditions/', 'control_files'));
mkdir(resultspath, strcat('Conditions/', 'gest2_files'));
mkdir(resultspath, strcat('Conditions/',  'gest3_files'));
mkdir(resultspath, strcat('Conditions/', 'imag2_files'));
mkdir(resultspath, strcat('Conditions/', 'imag3_files'));
mkdir(resultspath, strcat('Conditions/', 'word2_files'));
mkdir(resultspath, strcat('Conditions/', 'word3_files'));
mkdir(resultspath, strcat('Conditions/',  'Png_files'));


condList = {"control" "word2" "word3" "imag2" "imag3" "gest2" "gest3"};
freqInter = {"beat1" "beat2" "beat3" "beat4"}; % frequencies of interest
comps = {"allElec" "ress"};

for i = 1:length(condList)
    condAllElec.(condList{i}).comb = [];
end

% initializing structures for data
for m = 1:length(comps)
    for k = 1:length(freqInter)
        for j = 1:length(condList)
            power.(comps{m}).(freqInter{k}).(condList{j}).subs = [];
            power.(comps{m}).(freqInter{k}).(condList{j}).mean = [];
            zscored.(comps{m}).(freqInter{k}).(condList{j}).subs = [];
            zscored.(comps{m}).(freqInter{k}).(condList{j}).mean = [];
        end
    end
end


for i = 1:length(condList)
    for k = 1:length(pooledSets.(condList{i}))

             %====================================================%
             %========= pre-process data and compute FFT =========%
             %====================================================%
             
             % load set
             EEG = pop_loadset(pooledSets.(condList{i})(k).name, pooledSets.(condList{i})(k).folder);
             data = EEG.data(:,:,:);
             
             % extract name and file location
             setLocation = strcat(pooledSets.(condList{i})(k).folder, '/', pooledSets.(condList{i})(k).name);
             [~,setName] = fileparts(setLocation);
             
             % Average across trials
             data = mean(data, 3);
             
             % compute FFT and average across channels
             dataFFT = mean(abs( fft(data(:,:),nfft,2)/EEG.pnts ).^2,1);
             
             % write timeseries to structure containing all timeseries
             condAllElec.(condList{i}).comb = cat(1, condAllElec.(condList{i}).comb, dataFFT);  
             
             % SNR frequency-domain baseline subtraction
             normData = squeeze(dataFFT);
             for bin = (nBins + 1):(length(normData)-nBins)
                 binMean = mean([ dataFFT(bin - nBins), dataFFT(bin + nBins) ]);
                 normData(bin) = dataFFT(bin) - binMean;
             end
             
             %====================================================%
             %================= plot data and save ===============%
             %====================================================%
             
             % plot power FFT
             figure(1), clf
             xlim = [0 4];
             plot(hz,dataFFT,'LineWidth',2,'Color',[.6 0 0])
             hold on
             set(gca,'xlim',xlim)
             axis square
             xlabel('Frequency (Hz)'), ylabel('Power')
             %legend({'Freq plot';})
             title(strcat(setName, " all electrodes"));
             
             % save plot as png
             print(strcat(setName, "_all_elec"), '-dpng');
             movefile(strcat(setName, '_all_elec','.png'), strcat(resultspath, 'All_electrodes'));

             % plot FFT of freq-domain normalized data
             figure(2), clf
             xlim = [0 4];
             plot(hz, normData,'LineWidth',2,'Color',[.6 0 0])
             hold on
             set(gca,'xlim',xlim)
             axis square
             xlabel('Frequency (Hz)'), ylabel('Power')
             %legend({'Freq plot';})
             %annotation('textarrow', [0.2 0.8], [normData(ceil(2.4/freqRes)+1) 0.5]);
             title(strcat(setName, ' freq-domain normalized'));
             
             % save plot as png
             print(strcat(setName, '_norm_all_elec'), '-dpng')
             movefile(strcat(setName, '_norm_all_elec','.png'), strcat(resultspath, 'All_electrodes'));
             
             %====================================================%
             %===== extract freqs of interest and save data ======%
             %====================================================%
             
             % extract average power values at frequencies of interest
             beat1 = normData(ceil(2.4/freqRes));  % 2.4Hz
             beat2 = normData(ceil(1.2/freqRes));  % 1.2 Hz
             beat3 = normData(ceil(0.8/freqRes));  % 0.8 Hz
             beat4 = normData(ceil(1.6/freqRes));  % 1.6Hz
             
             beatMean = mean([beat1, beat2, beat3, beat4]);   
             beatSd = std([beat1, beat2, beat3, beat4]);
             
             % Logging z-scored values for frequencies of interest
             zscored.allElec.beat1.(condList{i}).subs = cat(2, zscored.allElec.beat1.(condList{i}).subs, ( (beat1 - beatMean)/beatSd) ); % 2.4hz   
             zscored.allElec.beat2.(condList{i}).subs = cat(2, zscored.allElec.beat2.(condList{i}).subs, ( (beat2 - beatMean)/beatSd) ); % 1.2Hz
             zscored.allElec.beat3.(condList{i}).subs = cat(2, zscored.allElec.beat3.(condList{i}).subs, ( (beat3 - beatMean)/beatSd) ); % 0.8Hz
             zscored.allElec.beat4.(condList{i}).subs = cat(2, zscored.allElec.beat4.(condList{i}).subs, ( (beat4 - beatMean)/beatSd) ); % 1.6hz
             
             % logging standard power values for frequencies of interest
             power.allElec.beat1.(condList{i}).subs = cat(2, power.allElec.beat1.(condList{i}).subs, beat1);
             power.allElec.beat2.(condList{i}).subs = cat(2, power.allElec.beat2.(condList{i}).subs, beat2);
             power.allElec.beat3.(condList{i}).subs = cat(2, power.allElec.beat3.(condList{i}).subs, beat3);
             power.allElec.beat4.(condList{i}).subs = cat(2, power.allElec.beat4.(condList{i}).subs, beat4);

    end
         
         %====================================================%
         %============== prepare pooled data =================%
         %====================================================%
         
         % compute mean 
         condAllElec.(condList{i}).mean = squeeze(mean(condAllElec.(condList{i}).comb, 1));  
         
         % SNR frequency-domain baseline subtraction
         normData = condAllElec.(condList{i}).mean;
         for bin = (nBins + 1):(length(normData)-nBins)
             binMean = mean([ condAllElec.(condList{i}).mean(bin - nBins), condAllElec.(condList{i}).mean(bin + nBins) ]);
             normData(bin) = condAllElec.(condList{i}).mean(bin) - binMean;
         end
         
         %====================================================%
         %================ plot pooled data ==================%
         %====================================================%
         
         % plotting mean ALL ELECTRODE FFT
         figure(3), clf
         subplot(2,1,1);
         xlim = [0 4];
         plot(hz, condAllElec.(condList{i}).mean,'LineWidth',2,'Color',[.6 0 0])
         hold on
         set(gca,'xlim',xlim)
         axis square
         xlabel('Frequency (Hz)'), ylabel('Power')
         title(strcat(condList{i}, " pooled subjects"));
 
         subplot(2,1,2);
         xlim = [0 4];
         plot(hz, normData,'LineWidth',2,'Color',[.6 0 0])
         hold on
         set(gca,'xlim',xlim)
         axis square
         xlabel('Frequency (Hz)'), ylabel('Power')
         title(strcat(condList{i}, ' normalized all elec'));
         
         % save plot as png
         print(strcat(convertStringsToChars(condList{i}), '_allElec_pooled'), '-dpng')
         movefile(strcat(convertStringsToChars(condList{i}), '_allElec_pooled','.png'), strcat(resultspath, 'All_electrodes'));
         
         %====================================================%
         %=========== extract freq data and save =============%
         %====================================================%
         % zscored means
         zscored.allElec.beat1.(condList{i}).mean = mean(zscored.allElec.beat1.(condList{i}).subs);
         zscored.allElec.beat2.(condList{i}).mean = mean(zscored.allElec.beat2.(condList{i}).subs);
         zscored.allElec.beat3.(condList{i}).mean = mean(zscored.allElec.beat3.(condList{i}).subs);
         zscored.allElec.beat4.(condList{i}).mean = mean(zscored.allElec.beat4.(condList{i}).subs);
         
         % power means
         power.allElec.beat1.(condList{i}).mean = mean(power.allElec.beat1.(condList{i}).subs);
         power.allElec.beat2.(condList{i}).mean = mean(power.allElec.beat2.(condList{i}).subs);
         power.allElec.beat3.(condList{i}).mean = mean(power.allElec.beat3.(condList{i}).subs);
         power.allElec.beat4.(condList{i}).mean = mean(power.allElec.beat4.(condList{i}).subs);
   
 end

% save all electrode data
         save("all_electrode", 'zscored', 'power');
         movefile('all_electrode.mat', strcat(resultspath, 'All_electrodes'));
         
%% ++++++++++++++++++++ PART 5: RESS ANALYSIS A +++++++++++++++++++++ %%
%+++++++++++++++++++++++++ CREATING POOLED SET ++++++++++++++++++++++++++%
%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%

datapath = '/Users/Stilts/MATLAB/data/Exp1_data/Processed/Part_3/';
resultspath = '/Users/Stilts/MATLAB/data/Exp1_data/Processed/Part_4/';
cd (datapath);
currentDir = (datapath);

condList = {'control' 'word2' 'word3' 'imag2' 'imag3' 'gest2' 'gest3'};

% Create lists of set files, organised by condition
for cond = 1:length(condList)
    pooledSets.(condList{cond}) = dir(strcat('**/*', condList{cond}, '*.set'));
end

% initializing combined data structure
dataComb = [];

% pool condition datasets across subjects into CondComb structure
for i = 1:length(condList)
    for k = 1:length(pooledSets.(condList{i}))
        EEG = pop_loadset(pooledSets.(condList{i})(k).name, pooledSets.(condList{i})(k).folder);
        data = EEG.data(:,:,:);
        dataComb = cat(3, data, dataComb);
    end
    CondComb.(condList{i}) = mean(dataComb(:,:,:), 3);
    dataComb = [];
end
%% ++++++++++++++++++++ PART 6: RESS ANALYSIS B +++++++++++++++++++++ %%
%+++++++++++++++++++++++ COMPUTING COMPONENTS ++++++++++++++++++++++++%
%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%

addpath '/Users/Stilts/MATLAB/code/Mikexcohen/ress' % to access FilterFGX function

for i = 1:length(condList)
    
    % FFT parameters
    freqRes = EEG.srate/EEG.pnts;
    nfft = ceil( EEG.srate/freqRes);
    
    if i == 1
        peakwidt  = .4;  % FWHM at peak frequency
        neighfreq = .3;  % distance of neighboring frequencies away from peak frequency, +/- in Hz
        neighwidt = .3;  % FWHM of the neighboring frequencies
        peakfreq = 2.4; % hz
    elseif i == 2 || i == 4 || i == 6 % binary conditions
        peakwidt  = .4;  % FWHM at peak frequency .15
        neighfreq = .3;  % distance of neighboring frequencies away from peak frequency, +/- in Hz .2
        neighwidt = .3;  % FWHM of the neighboring frequencies .15
        peakfreq = 1.2; % hz
    else % ternary conditions
        peakwidt  = .3;  % FWHM at peak frequency
        neighfreq = .2;  % distance of neighboring frequencies away from peak frequency, +/- in Hz
        neighwidt = .2;  % FWHM of the neighboring frequencies
        peakfreq = 0.8; % hz
    end
    
    
    % define data
    data  = CondComb.(condList{i})(:,:);
    dataX = abs( fft(data(:,:),nfft,2)/EEG.pnts ).^2;
    hz    = linspace(0,EEG.srate,nfft);
    
    % compute covariance matrix at peak frequency
    fdatAt = filterFGx(data,EEG.srate,peakfreq,peakwidt);
    fdatAt = reshape( fdatAt(:,:,:), EEG.nbchan,[] );
    fdatAt = bsxfun(@minus,fdatAt,mean(fdatAt,2));
    covAt  = (fdatAt*fdatAt')/EEG.pnts;
    
    % compute covariance matrix for lower neighbour
    fdatLo = filterFGx(data,EEG.srate,peakfreq+neighfreq,neighwidt);
    fdatLo = reshape( fdatLo(:,:,:), EEG.nbchan,[] );
    fdatLo = bsxfun(@minus,fdatLo,mean(fdatLo,2));
    covLo  = (fdatLo*fdatLo')/EEG.pnts;
    
    % compute covariance matrix for upper neighbour
    fdatHi = filterFGx(data,EEG.srate,peakfreq-neighfreq,neighwidt);
    fdatHi = reshape( fdatHi(:,:,:), EEG.nbchan,[] );
    fdatHi = bsxfun(@minus,fdatHi,mean(fdatHi,2));
    covHi  = (fdatHi*fdatHi')/EEG.pnts;
    
    % perform generalized eigendecomposition.
    [evecs,evals] = eig(covAt,(covHi+covLo)/2);
    [~,comp2plot] = max(diag(evals)); % find maximum component
    evecs = bsxfun(@rdivide,evecs,sqrt(sum(evecs.^2,1))); % normalize vectors
    
    % extract components and force sign
    maps = covAt * evecs / (evecs' * covAt * evecs);
    [~,idx] = max(abs(maps(:,comp2plot))); % find biggest component
    maps = maps * sign(maps(idx,comp2plot)); % force to positive sign
    
    % save components to structure
    ressComps.(condList{i}).evecs = evecs;
    ressComps.(condList{i}).evals = evals;
    ressComps.(condList{i}).comp2plot = comp2plot;
    ressComps.(condList{i}).maps = maps;
    
end

%% ++++++++++++++++++++ PART 6: RESS ANALYSIS C +++++++++++++++++++++ %%
%++++++++++++++++++++ PLOTS AND FREQ EXTRACTION +++++++++++++++++++++++%
%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%

datapath = '/Users/Stilts/MATLAB/data/Exp1_data/Processed/Part_3/';
resultspath = '/Users/Stilts/MATLAB/data/Exp1_data/Processed/Part_4/';
cd (datapath);
currentDir = (datapath);

nBins = 2; % for freqdomain baseline subtration: how many bins either side to substract avg?    ##### this should be kept the same as in the ALL ELECTRODE ANALYSIS

for i = 1:length(condList)
    condRessx.(condList{i}).comb = [];
    for k = 1:length(pooledSets.(condList{i}))
        %====================================================%
        %============ preprocess and compute FFT ============%
        %====================================================%
        
        % load dataset
        EEG = pop_loadset(pooledSets.(condList{i})(k).name, pooledSets.(condList{i})(k).folder);
        data = EEG.data(:,:,:);
        
        % set locationa and filenames
        setLocation = strcat(pooledSets.(condList{i})(k).folder, '/', pooledSets.(condList{i})(k).name);
        [~,setName] = fileparts(setLocation);
        
        % reconstruct RESS component time series
        ress_ts = zeros(EEG.nbchan, EEG.pnts, size(data,3));  % initialize matrix as zeros
        for ti=1:size(data,3)  % for each trial
            for k = 1:EEG.nbchan  % for each channel
                ress_ts(k,:,ti) = ressComps.(condList{i}).evecs(:,ressComps.(condList{i}).comp2plot)'*squeeze(data(:,:,ti));
            end
        end
        
        % Average across trials
        ress_ts = mean(ress_ts, 3);
        
        % compute FFT and average across channels
        ressx = mean(abs( fft(ress_ts(:,:),nfft,2)/EEG.pnts ).^2,1);
        
        condRessx.(condList{i}).comb = cat(1, condRessx.(condList{i}).comb, ressx);  % write RESS timeseries to structure containing all RESS TSs
        
        % SNR frequency-domain baseline subtraction
        normData = squeeze(ressx);
        for bin = (nBins + 1):(length(normData)-nBins)
            binMean = mean([ ressx(bin - nBins), ressx(bin + nBins) ]);
            normData(bin) = ressx(bin) - binMean;
        end
        
        %====================================================%
        %================== Plot and save ===================%
        %====================================================%
        
        % Plot FFT of RESS component
        figure(1), clf
        xlim = [0 4];
        subplot(2,1,1);
        plot(hz,ressx,'LineWidth',2,'Color',[.6 0 0])
        hold on
        set(gca,'xlim',xlim)
        axis square
        xlabel('Frequency (Hz)'), ylabel('Power')
        title(setName);
        
        % Plot forward model of RESS component as scalp map
        subplot(2,1,2);
        topoplot(ressComps.(condList{i}).maps(:, ressComps.(condList{i}).comp2plot),EEG.chanlocs);
        title(strcat(setName, ' headplot'));
        
        % save plot as png
        print(setName, '-dpng');
        movefile(strcat(setName,'.png'), strcat(resultspath, 'RESS'));
        
        % Plot freq-domain normalized data
        figure(2), clf
        xlim = [0 4];
        plot(hz, normData,'LineWidth',2,'Color',[.6 0 0])
        hold on
        set(gca,'xlim',xlim)
        axis square
        xlabel('Frequency (Hz)'), ylabel('Power')
        title(strcat(setName, ' freq-domain normalized'));
        
        % save plot as png
        print(strcat(setName, '_norm'), '-dpng')
        movefile(strcat(setName, '_norm','.png'), strcat(resultspath, 'RESS'));
        
        %====================================================%
        %=========== extract freq data and save =============%
        %====================================================%
        
        % extract average power values at frequencies of interest
        beat1 = normData(ceil(2.4/freqRes));  % 2.4Hz
        beat2 = normData(ceil(1.2/freqRes));  % 1.2 Hz
        beat3 = normData(ceil(0.8/freqRes));  % 0.8 Hz
        beat4 = normData(ceil(1.6/freqRes));  % 1.6Hz
        
        beatMean = mean([beat1, beat2, beat3, beat4]);
        beatSd = std([beat1, beat2, beat3, beat4]);
        
        % Logging z-scored values for frequencies of interest
        zscored.ress.beat1.(condList{i}).subs = cat(2, zscored.ress.beat1.(condList{i}).subs, ( (beat1 - beatMean)/beatSd) ); % 2.4hz
        zscored.ress.beat2.(condList{i}).subs = cat(2, zscored.ress.beat2.(condList{i}).subs, ( (beat2 - beatMean)/beatSd) ); % 1.2Hz
        zscored.ress.beat3.(condList{i}).subs = cat(2, zscored.ress.beat3.(condList{i}).subs, ( (beat3 - beatMean)/beatSd) ); % 0.8Hz
        zscored.ress.beat4.(condList{i}).subs = cat(2, zscored.ress.beat4.(condList{i}).subs, ( (beat4 - beatMean)/beatSd) ); % 1.6hz
        
        % logging standard power values for frequencies of interest
        power.ress.beat1.(condList{i}).subs = cat(2, power.ress.beat1.(condList{i}).subs, beat1);
        power.ress.beat2.(condList{i}).subs = cat(2, power.ress.beat2.(condList{i}).subs, beat2);
        power.ress.beat3.(condList{i}).subs = cat(2, power.ress.beat3.(condList{i}).subs, beat3);
        power.ress.beat4.(condList{i}).subs = cat(2, power.ress.beat4.(condList{i}).subs, beat4);
        
        %              % save RESS fft data
        %              save(strcat(setName, '_ress_vars'), 'ressx', 'ressComps', 'ress_ts');
        %              movefile(strcat(setName,'_ress_vars.mat'), strcat(resultspath, 'Conditions/', condList{i}, '_files', '/'));
    end
    
    %====================================================%
    %============= PREPROCESS POOLED DATA ===============%
    %====================================================%
    
    % pooled RESS FFT conditions across subjects
    condRessx.(condList{i}).mean = squeeze(mean(condRessx.(condList{i}).comb, 1));
    
    % SNR frequency-domain baseline subtraction
    normData = condRessx.(condList{i}).mean;
    for bin = (nBins + 1):(length(normData)-nBins)
        binMean = mean([ condRessx.(condList{i}).mean(bin - nBins), condRessx.(condList{i}).mean(bin + nBins) ]);
        normData(bin) = condRessx.(condList{i}).mean(bin) - binMean;
    end
    
    %====================================================%
    %============= PLOT POOLED RESS DATA ================%
    %====================================================%
    
    % plotting mean RESS ts
    figure(3), clf
    xlim = [0 4];
    subplot(2,1,1);
    plot(hz, condRessx.(condList{i}).mean,'LineWidth',2,'Color',[.6 0 0])
    hold on
    set(gca,'xlim',xlim)
    axis square
    xlabel('Frequency (Hz)'), ylabel('Power')
    title(strcat(condList{i}, " pooled"));
    
    % Plot forward model fo RESS component as scalp map
    subplot(2,1,2);
    topoplot(-(ressComps.(condList{i}).maps(:, ressComps.(condList{i}).comp2plot)),EEG.chanlocs);  % switched sign to minus to fix polarity problem   ###########
    title(strcat(condList{i}, ' headplot'));
    
    % save plot as png
    print(strcat(condList{i}, "_pooled"), '-dpng')
    movefile(strcat(condList{i}, '_pooled','.png'), strcat(resultspath, 'RESS'));
    
    figure(4), clf
    xlim = [0 4];
    plot(hz, normData,'LineWidth',2,'Color',[.6 0 0])
    hold on
    set(gca,'xlim',xlim)
    axis square
    xlabel('Frequency (Hz)'), ylabel('Power')
    title(strcat(condList{i}, ' freq-domain normalized'));
    
    % save plot as png
    print(strcat(condList{i}, '_norm'), '-dpng')
    movefile(strcat(condList{i}, '_norm','.png'), strcat(resultspath, 'RESS'));
    
    %====================================================%
    %======== extract pooled freq data and save =========%
    %====================================================%
    
    % zscored means
    zscored.ress.beat1.(condList{i}).mean = mean(zscored.ress.beat1.(condList{i}).subs);
    zscored.ress.beat2.(condList{i}).mean = mean(zscored.ress.beat2.(condList{i}).subs);
    zscored.ress.beat3.(condList{i}).mean = mean(zscored.ress.beat3.(condList{i}).subs);
    zscored.ress.beat4.(condList{i}).mean = mean(zscored.ress.beat4.(condList{i}).subs);
    
    % power means
    power.ress.beat1.(condList{i}).mean = mean(power.ress.beat1.(condList{i}).subs);
    power.ress.beat2.(condList{i}).mean = mean(power.ress.beat2.(condList{i}).subs);
    power.ress.beat3.(condList{i}).mean = mean(power.ress.beat3.(condList{i}).subs);
    power.ress.beat4.(condList{i}).mean = mean(power.ress.beat4.(condList{i}).subs);
end

% save RESS fft data
save('RESS', 'zscored', 'power');
movefile('RESS.mat', strcat(resultspath, 'RESS'));