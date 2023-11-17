import React, { useState } from 'react';
import { useFormik } from 'formik';
import {
  Box,
  Button,
  Container,
  Stack,
  SvgIcon,
  Typography,
  TextField,
  MenuItem,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import PlusIcon from '@heroicons/react/24/solid/PlusIcon';
import { createCategory } from 'src/api/api';
import { getCategories } from 'src/api/api';
import { toast } from 'react-toastify';

const MyForm = ( {setCategories}) => {
  const formik = useFormik({
    initialValues: {
      product_description: '',
      weighting_type: 'quality-price',
    },
    onSubmit: async (values)  => {
      values.excludes = excluirList;
      const id = toast.loading("Generando recomendaciones. Esto puede durar varios minutos...")
      try {
        await createCategory(values);
        getCategories().then((response) => {
          setCategories(response.data);
        });
        toast.update(id, { render: "Error en generar recomendaciones", type: "error", isLoading: false,  closeButton: true });
      } catch (error) {
        console.log(error);
      }
      toast.update(id, { render: "Recomendaciones generadas con exito", type: "success", isLoading: false, closeButton: true });
    },
  });

  const [excluirList, setExcluirList] = useState([]);
  const [currentExcluir, setCurrentExcluir] = useState('');

  const handleAddExcluir = () => {
    if (currentExcluir.trim() !== '') {
      setExcluirList([...excluirList, currentExcluir]);
      setCurrentExcluir('');
    }
  };

  return (
    <form onSubmit={formik.handleSubmit}>
      <TextField
        fullWidth
        label="Categoría del producto ó descripción"
        name="product_description"
        value={formik.values.product_description}
        onChange={formik.handleChange}
        variant="outlined"
        margin="normal"
      />

      <TextField
        fullWidth
        select
        label="Ponderación"
        name="weighting_type"
        value={formik.values.weighting_type}
        onChange={formik.handleChange}
        variant="outlined"
        margin="normal"
      >
        <MenuItem value="quality">Calidad</MenuItem>
        <MenuItem value="price">Precio</MenuItem>
        <MenuItem value="quality-price">Calidad-Precio</MenuItem>
      </TextField>

      {/* Campo de entrada de texto para agregar strings a la lista */}
      <TextField
        fullWidth
        label="Excluir en la busqueda (Agregar strings uno por uno)"
        name="excludes"
        value={currentExcluir}
        onChange={(e) => setCurrentExcluir(e.target.value)}
        variant="outlined"
        margin="normal"
      />
      <Button
        onClick={handleAddExcluir}
        variant="contained"
        color="primary"
      >
        Agregar
      </Button>

      {/* Lista de strings excluidos */}
      <List>
        {excluirList.map((item, index) => (
          <ListItem key={index}>
            <ListItemText primary={item} />
          </ListItem>
        ))}
      </List>

      <Button
        startIcon={(
          <SvgIcon fontSize="small">
            <PlusIcon />
          </SvgIcon>
        )}
        variant="contained"
        type="submit"
      >
        Agregar producto a mi lista de deseos
      </Button>
    </form>
  );
};


export default MyForm;
