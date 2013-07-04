function vocabList = getVocabList()
%GETVOCABLIST reads the fixed vocabulary list in vocab.txt and returns a
%cell array of the words
%   vocabList = GETVOCABLIST() reads the fixed vocabulary list in vocab.txt 
%   and returns a cell array of the words in vocabList.


%% Read the fixed vocabulary list
fid = fopen('vocab.txt');

% Store all dictionary words in cell array vocab{}
n = 1899;  % Total number of words in the dictionary


vocabList = java.util.HashMap;
for i = 1:n
    % Word Index (can ignore since it will be = i)
    idx = fscanf(fid, '%d', 1);
    % Actual Word
    vocabList.put(fscanf(fid, '%s', 1), idx);
end
fclose(fid);

end
