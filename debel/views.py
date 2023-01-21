from django.shortcuts import render, redirect
from .forms import laymanForm
from .musicWork.createMusic import saveMidi, BITS_PER_NOTE, changeInstrument
from .musicWork.algorithms import initialPopulationGeneration, selectionProcess, crossoverFunction, mutation, chromosomeToString, stringtoChromosome
from django.contrib import messages
import shutil, os
# Create your views here.

def home(request):
    return render(request, 'debel/home.html')

def about(request):
    return render(request, 'debel/about.html', {'title': 'About'})

def layman(request):
    print(request)
    if request.method == "POST":
        form = laymanForm(request.POST)
        if form.is_valid():
            mood = form.cleaned_data.get('mood')
            bpm = int(form.cleaned_data.get('bpm'))
            instrument = form.cleaned_data.get('instrument')
            print("Before Layman",request)
            request.session["mood"] = mood
            request.session["bpm"] = bpm
            request.session["instrument"] = instrument
            return redirect('debel_music_layman')
    else:
        form = laymanForm()
    return render(request, 'debel/layman.html', {'title': "Layman's Corner", "form":form})

def virtuoso(request):
    return render(request, 'debel/virtuoso.html', {'title': "Virtuoso's Studio"})

def expert(request):
    return render(request, 'debel/expert.html', {'title': "Expert's Lab"})

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
            saveMidi(filename="static/" + filePath, numTracks=numTracks, numBars=numBars, gene=child, bpm=bpm, isPause=isPause, key=key, scale=scale, scaleRoot=scaleRoot, sig=sig)
            changeInstrument("static/"+filePath, "Instrument", instrument)
            if childStr not in geneToFile.keys():
                geneToFile[childStr] = filePath
        return geneToFile
    
    #After Form Submit
    if request.method=="POST":
        # Submitting the ratings of music
        if request.POST.get("rateSubmit"):
            messages.success(request, 'Thank you for rating the music!!\nYour work is in progress.')
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
            # for i in pairsListofParents:
            #     p1, p2 = i
            #     if p1 not in nextGeneration:
            #         nextGeneration.append(p1)
            #     if p2 not in nextGeneration:
            #         nextGeneration.append(p2)
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

