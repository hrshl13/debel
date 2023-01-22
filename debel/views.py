from django.shortcuts import render, redirect
from .forms import laymanForm, virtuosoForm, expertForm
from .musicWork.createMusic import saveMidi, BITS_PER_NOTE, changeInstrument
from .musicWork.algorithms import initialPopulationGeneration, selectionProcess, crossoverFunction, mutation, chromosomeToString, stringtoChromosome
from django.contrib import messages
import shutil, os
# Create your views here.
from .musicWork.createMusic import TIME_SIGNATURE_TO_BEATS
def home(request):
    return render(request, 'debel/home.html')

def about(request):
    return render(request, 'debel/about.html', {'title': 'About'})

def layman(request):
    if request.method == "POST":
        form = laymanForm(request.POST)
        if form.is_valid():
            formObj = form.cleaned_data
            request.session["mood"] = formObj.get('mood')
            request.session["bpm"] = formObj.get('bpm')
            request.session["instrument"] = formObj.get('instrument')
            return redirect('debel_music_layman')
    else:
        form = laymanForm()
    return render(request, 'debel/layman.html', {'title': "Layman's Corner", "form":form})

def LaymanLoadMusic(request):
    # Get the user input from previous form using sessions
    mood = request.session["mood"]
    bpm = int(request.session["bpm"])
    instrument = request.session["instrument"]
    # Algorithm starts
    ## Pre-Settings for Algorithm other than user input  
    scale="major"
    if mood=="Sad":
        scale = "minorH"
    numOctaves=2
    isPause=False
    numBars=8
    notesPerBar=4
    numTracks = 2
    populationSize=5
    key="C"
    scaleRoot=4
    sig="4/4"
    def gtfCreation(population:list):
        """
        It saves the midi file of the music generated from the population, and then returns a dictionary containing the genes of the population as it's keys and the corresponding file path of the midi file genrated from the said gene.

        Args:
            population (list): List of genes from the population madeup of bit strings created for generating music.

        Returns:
           dict: A dictionary of genes and their corresponding midi file paths.
        """
        geneToFile={}
        folder = "laymanMusic/"
        if os.path.isdir("static/"+folder):
            shutil.rmtree("static/"+folder)
        for index, child in enumerate(population):
            childStr = chromosomeToString(child)
            fileName =  f"{index+1}.mid"
            filePath =  folder + fileName
            saveMidi(filename="static/" + filePath, numOctaves=numOctaves, numTracks=numTracks, numBars=numBars, gene=child, bpm=bpm, isPause=isPause, key=key, scale=scale, scaleRoot=scaleRoot, sig=sig)
            changeInstrument("static/"+filePath, "Instrument", instrument)
            if childStr not in geneToFile.keys():
                geneToFile[childStr] = filePath
        return geneToFile
    
    #After Form Submit
    if request.method=="POST":
        # Submitting the ratings of music
        if request.POST.get("rateSubmit"):
            DSfit = []
            # Accessing geneToFile
            geneToFile = request.session["gtf"]
            # Accessing each gene's(music's) rating from user and making a list of tuples having the gene and rating as their values.  
            for gene in geneToFile.keys():
                fitness = request.POST.get(gene)
                if fitness=="":
                    fitness=1
                else:
                    try: 
                        fitness = int(fitness)
                    except:
                        fitness = 1
                chromosome =  stringtoChromosome(gene)
                DSfit.append((chromosome, fitness))
            assert len(geneToFile)==len(DSfit)
            #Selecton Process
            selectionIndex=0  # Roulette Selection
            pairsListofParents  = selectionProcess(fds = DSfit, index = selectionIndex, populationSize=populationSize)
            # (MU, LAMBDA) Evolution Strategy
            nextGeneration=[]
            #Crossover 
            crossIndex = 0  #Single Point Crossover
            for i in pairsListofParents:
                child1, child2 = crossoverFunction(a = i[0], b = i[1], index=crossIndex)
                nextGeneration.append(child1)
                nextGeneration.append(child2)
            #Mutation 
            probab = 0.5
            mutNum = 5
            for nextChromo in nextGeneration:
                nextChromo = mutation(nextChromo, probab, mutNum)
            #Generation Complete
            population = nextGeneration
            #Creating children music files
            geneToFile = gtfCreation(population)
            request.session["gtf"] = geneToFile
            # Asking Fitness for next generation
            return render(request, 'debel/loadMusic.html', {'genetoFile':geneToFile})    
        #if Termination == True
        elif request.POST.get("stopGen"):
            shutil.rmtree("static/laymanMusic/")
            try:
                del request.session['mood']
                del request.session['instrument']
                del request.session['bpm']
                del request.session['gtf']
            except KeyError:
                pass
            return redirect("debel_home")
    # If calling this form for the first time
    else:    
        # Genertaing initial population
        population = initialPopulationGeneration(populationSize,numBars * notesPerBar * BITS_PER_NOTE)
        # A dictionary with genes(bit string) as keys and their corresponding midi file paths.
        geneToFile = gtfCreation(population)
        #Phase 1 completes
        request.session["gtf"] = geneToFile
        return render(request, 'debel/loadMusic.html', {'genetoFile':geneToFile})

def virtuoso(request):
    if request.method == "POST":
        form = virtuosoForm(request.POST)
        if form.is_valid():
            formObj = form.cleaned_data
            request.session["numBars"] = formObj.get('numBars')
            request.session["timeSig"] = formObj.get('timeSig')
            request.session["bpm"] = formObj.get('bpm')
            request.session["keyNote"] = formObj.get('keyNote')
            request.session["scale"] = formObj.get('scale')
            request.session["rootOctave"] = formObj.get('rootOctave')
            request.session["pauses"] = formObj.get('pauses')
            request.session["numOctaves"] = formObj.get('numOctaves')
            request.session["numTracks"] = formObj.get('numTracks')
            request.session["instrument"] = formObj.get('instrument')
            return redirect('debel_music_virtuoso')
    else:
        form = virtuosoForm()
        return render(request, 'debel/virtuoso.html', {'title': "Virtuoso's Studio", "form":form})

def VirtuosoLoadMusic(request):
    numBars = int(request.session["numBars"])
    timeSig = request.session["timeSig"]
    bpm = int(request.session["bpm"])
    keyNote = request.session["keyNote"]
    scale = request.session["scale"]
    rootOctave = float(request.session["rootOctave"])
    pauses = bool(request.session["pauses"])
    numOctaves = int(request.session["numOctaves"])
    numTracks = int(request.session["numTracks"])
    instrument = request.session["instrument"]
    populationSize=5
    
    def gtfCreation(population:list):
        """
        It saves the midi file of the music generated from the population, and then returns a dictionary containing the genes of the population as it's keys and the corresponding file path of the midi file genrated from the said gene.

        Args:
            population (list): List of genes from the population madeup of bit strings created for generating music.

        Returns:
           dict: A dictionary of genes and their corresponding midi file paths.
        """
        geneToFile={}
        folder = "virtuosoMusic/"
        if os.path.isdir("static/"+folder):
            shutil.rmtree("static/"+folder)
        for index, child in enumerate(population):
            childStr = chromosomeToString(child)
            fileName =  f"{index+1}.mid"
            filePath =  folder + fileName
            saveMidi(filename="static/" + filePath, numOctaves=numOctaves, numTracks=numTracks, numBars=numBars, gene=child, bpm=bpm, isPause=pauses, key=keyNote, scale=scale, scaleRoot=rootOctave, sig=timeSig)
            changeInstrument("static/"+filePath, "Instrument", instrument)
            if childStr not in geneToFile.keys():
                geneToFile[childStr] = filePath
        return geneToFile
    
    #After Form Submit
    if request.method == "POST":
        # Submitting the ratings of music
        if request.POST.get("rateSubmit"):
            DSfit = []
            # Accessing geneToFile
            geneToFile = request.session["gtf"]
            # Accessing each gene's(music's) rating from user and making a list of tuples having the gene and rating as their values.  
            for gene in geneToFile.keys():
                fitness = request.POST.get(gene)
                if fitness=="":
                    fitness=1
                else:
                    try: 
                        fitness = int(fitness)
                    except:
                        fitness = 1
                chromosome =  stringtoChromosome(gene)
                DSfit.append((chromosome, fitness))
            assert len(geneToFile)==len(DSfit)
            #Selecton Process
            selectionIndex=0  # Roulette Selection
            pairsListofParents  = selectionProcess(fds = DSfit, index = selectionIndex, populationSize=populationSize)
            # (MU, LAMBDA) Evolution Strategy
            nextGeneration=[]
            #Crossover 
            crossIndex = 0  #Single Point Crossover
            for i in pairsListofParents:
                child1, child2 = crossoverFunction(a = i[0], b = i[1], index=crossIndex)
                nextGeneration.append(child1)
                nextGeneration.append(child2)
            #Mutation 
            probab = 0.5
            mutNum = 5
            for nextChromo in nextGeneration:
                nextChromo = mutation(nextChromo, probab, mutNum)
            #Generation Complete
            population = nextGeneration
            #Creating children music files
            geneToFile = gtfCreation(population)
            request.session["gtf"] = geneToFile
            # Asking Fitness for next generation
            return render(request, 'debel/loadMusic.html', {'genetoFile':geneToFile})    
        #if Termination == True
        elif request.POST.get("stopGen"):
            if os.path.isdir("static/"+"virtuosoMusic/"):
                shutil.rmtree("static/"+"virtuosoMusic/")
            try:
                del request.session
                # del request.session['instrument']
                # del request.session['bpm']
                # del request.session['gtf']
            except KeyError:
                pass
            return redirect("debel_home")
    # If calling this form for the first time
    else:
        # Genertaing initial population
        population = initialPopulationGeneration(populationSize,numBars * TIME_SIGNATURE_TO_BEATS[timeSig] * BITS_PER_NOTE)
        # A dictionary with genes(bit string) as keys and their corresponding midi file paths.
        geneToFile = gtfCreation(population)
        #Phase 1 completes
        request.session["gtf"] = geneToFile
        return render(request, 'debel/loadMusic.html', {'genetoFile':geneToFile})
    
def expert(request):
    if request.method == "POST":
        form = expertForm(request.POST)
        if form.is_valid():
            eformObj = form.cleaned_data
            request.session["numBars"] = eformObj.get('numBars')
            request.session["timeSig"] = eformObj.get('timeSig')
            request.session["mood"] = eformObj.get('mood')
            request.session["bpm"] = eformObj.get('bpm')
            request.session["evoStrat"] = eformObj.get('evoStrat')
            request.session["populationSize"] = eformObj.get('populationSize')
            request.session["selectionMethod"] = eformObj.get('selectionMethod')
            request.session["crossoverMethod"] = eformObj.get('crossoverMethod')
            request.session["mutNum"] = eformObj.get('mutNum')
            request.session["mutProb"] = eformObj.get('mutProb')
            request.session["instrument"] = eformObj.get('instrument')
            return redirect('debel_music_expert')
    else:
        form = expertForm()
        return render(request, 'debel/expert.html', {'title': "Expert's Lab", "form":form})

def ExpertLoadMusic(request):
    numBars = int(request.session["numBars"])
    timeSig = request.session["timeSig"]
    bpm = int(request.session["bpm"])
    mood = request.session["mood"]
    evoStrat = int(request.session["evoStrat"])
    populationSize = int(request.session["populationSize"])
    selectionMethod = int(request.session["selectionMethod"])
    crossoverMethod = int(request.session["crossoverMethod"])
    mutNum = int(request.session["mutNum"])
    mutProb = float(request.session["mutProb"])
    instrument = request.session["instrument"]
    scale = "major"
    if mood=="Sad":
        scale = "minorM"
    numOctaves = 3
    numTracks = 2
    pauses = False
    keyNote = "C"
    rootOctave = 4

    def gtfCreation(population:list):
        """
        It saves the midi file of the music generated from the population, and then returns a dictionary containing the genes of the population as it's keys and the corresponding file path of the midi file genrated from the said gene.

        Args:
            population (list): List of genes from the population madeup of bit strings created for generating music.

        Returns:
           dict: A dictionary of genes and their corresponding midi file paths.
        """
        geneToFile={}
        folder = "expertMusic/"
        if os.path.isdir("static/"+folder):
            shutil.rmtree("static/"+folder)
        for index, child in enumerate(population):
            childStr = chromosomeToString(child)
            fileName =  f"{index+1}.mid"
            filePath =  folder + fileName
            saveMidi(filename="static/" + filePath, numOctaves=numOctaves, numTracks=numTracks, numBars=numBars, gene=child, bpm=bpm, isPause=pauses, key=keyNote, scale=scale, scaleRoot=rootOctave, sig=timeSig)
            changeInstrument("static/"+filePath, "Instrument", instrument)
            if childStr not in geneToFile.keys():
                geneToFile[childStr] = filePath
        return geneToFile    
    
    if request.method == "POST":
        # Submitting the ratings of music
        if request.POST.get("rateSubmit"):
            DSfit = []
            # Accessing geneToFile
            geneToFile = request.session["gtf"]
            # Accessing each gene's(music's) rating from user and making a list of tuples having the gene and rating as their values.  
            for gene in geneToFile.keys():
                fitness = request.POST.get(gene)
                if fitness=="":
                    fitness=1
                else:
                    try: 
                        fitness = int(fitness)
                    except:
                        fitness = 1
                chromosome =  stringtoChromosome(gene)
                DSfit.append((chromosome, fitness))
            assert len(geneToFile)==len(DSfit)
            #Selecton Process
            pairsListofParents  = selectionProcess(fds = DSfit, index = selectionMethod, populationSize=populationSize)
            # Evolution Strategy
            nextGeneration=[]
            if evoStrat==0: #(MU + LAMBDA)
                for i in pairsListofParents:
                    p1, p2 = i
                    if p1 not in nextGeneration:
                        nextGeneration.append(p1)
                    if p2 not in nextGeneration:
                        nextGeneration.append(p2)
            elif evoStrat==1: # (MU, LAMBDA)
                pass
            #Crossover 
            for i in pairsListofParents:
                child1, child2 = crossoverFunction(a = i[0], b = i[1], index=crossoverMethod)
                nextGeneration.append(child1)
                nextGeneration.append(child2)
            #Mutation 
            for nextChromo in nextGeneration:
                nextChromo = mutation(nextChromo, mutProb, mutNum)
            #Generation Complete
            population = nextGeneration
            #Creating children music files
            geneToFile = gtfCreation(population)
            request.session["gtf"] = geneToFile
            # Asking Fitness for next generation
            return render(request, 'debel/loadMusic.html', {'genetoFile':geneToFile})    
        #if Termination == True
        elif request.POST.get("stopGen"):
            if os.path.isdir("static/"+"expertMusic/"):
                shutil.rmtree("static/"+"expertMusic/")
            try:
                del request.session
            except KeyError:
                pass

            return redirect("debel_home")
    # If calling this form for the first time        
        pass
    else:
        # Genertaing initial population
        population = initialPopulationGeneration(populationSize,numBars * TIME_SIGNATURE_TO_BEATS[timeSig] * BITS_PER_NOTE)
        # A dictionary with genes(bit string) as keys and their corresponding midi file paths.
        geneToFile = gtfCreation(population)
        #Phase 1 completes
        request.session["gtf"] = geneToFile
        return render(request, 'debel/loadMusic.html', {'genetoFile':geneToFile})